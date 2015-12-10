print(__doc__)

import db_tools
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.linear_model import SGDClassifier
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cross_validation import train_test_split


class question_group(object):

    def build_object(self, d):
        body = d[0]
        bodylen = len(body)
        score = d[1]
        commcount = d[2]
        sentipolarity = d[3]
        sentisubjectivity = d[4]
        links = d[5]
        promptness = d[6]
        acceptedanswer = d[7]
        if (acceptedanswer == None):
            aa = 0
        else:
            aa = int(acceptedanswer)
        qid = d[8]
        id = d[9]

        return [bodylen,score,commcount,sentipolarity,sentisubjectivity,links,promptness,aa]



def get_data():
    connection = db_tools.connect()
    cur = connection.cursor()

    q_group = question_group()
    master_map = defaultdict(int)

    # get all data necessary to train
    cur.execute("SELECT body,score,commcount,bodysentipolarity,bodysentisubjectivity,links,promptness,acceptedanswer,pid,id FROM answers")

    while True:
        data = cur.fetchone()
        if data == None:
            break

        q_id = data[8]
        if master_map[q_id] == 0:
            master_map[q_id] = [q_group.build_object(data)]
        else:
            master_map[q_id].append(q_group.build_object(data))

    #print master_map
    #print "\n\n\n\n\n\n"
    return master_map


def split_x_y(t):
    data = t.values()

    x_train = []
    y_train = []

    for answers in data:
        for answer in answers:
            x_train.append(answer[:len(answer)-1])
            y_train.append(answer[len(answer)-1:][0])

    return x_train, y_train

def train_model(t):
    # fit the model
    clf = SGDClassifier(loss="hinge", alpha=0.01, n_iter=200, fit_intercept=True)

    x_train, y_train = split_x_y(t)

    return clf.fit(x_train, y_train)

def test_model(model,t):
    results = []

    for qid, answers in t.iteritems():
        for answer in answers:
            x_test = answer[:len(answer)-1]
            y_test = answer[len(answer)-1:][0]
            p = model.decision_function([x_test])

            results.append((p[0],y_test))

            #if y_test == 1:
            print "pred: %d, actual: %i" % (p,y_test)
        print ""

    return results

def getKey(item):
     return item[0]

if __name__=='__main__':
    # we create 50 separable points
    master_map = get_data()
    train_map = {}
    test_map = {}

    idx = 0
    for key, val in master_map.iteritems():
        if idx % 4 == 0:
            test_map[key] = val
        else:
            train_map[key] = val
        idx += 1

    model = train_model(train_map)
    results = test_model(model,test_map)


    sorted(results, key=getKey)

    indx = 0
    for result in results:
        indx += 1
        print indx
        print result
