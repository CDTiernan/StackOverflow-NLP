# Author: Rob Zinkov <rob at zinkov dot com>
# License: BSD 3 clause

import db_tools

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn import datasets

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import LogisticRegression


def get_data():
    x_feats = 7
    y_feats = 1

    build_X = np.ndarray(shape=(2041,x_feats), dtype=float, order='C')
    build_y = np.ndarray(shape=(2041,), dtype=float, order='C')

    connection = db_tools.connect()
    cur = connection.cursor()

    cur.execute("SELECT body,score,commcount,bodysentipolarity,bodysentisubjectivity, links, promptness, acceptedanswer FROM answers")

    x_indx = 0
    y_indx = 0
    while True:
        data = cur.fetchone()
        if data == None:
            break

        body = data[0]
        bodylen = len(body)
        score = data[1]
        commcount = data[2]
        sentipolarity = data[3]
        sentisubjectivity = data[4]
        links = data[5]
        promptness = data[6]
        acceptedanswer = data[7]
        if acceptedanswer == None:
            aa = 0
        else:
            aa = 1

        np.put(build_X, [range(x_indx,x_indx + x_feats)], [bodylen,score,commcount,sentipolarity,sentisubjectivity,links,promptness]) #bodylen,score,commcount,sentipolarity,sentisubjectivity,links,promptness
        np.put(build_y, [range(y_indx,y_indx + y_feats)], [aa])

        x_indx += x_feats
        y_indx += y_feats

    return build_X, build_y

def classify():
    #for name, clf in classifiers:
    for numIter in range(10,110, 10):
        clf.set_params(n_iter=numIter)

        print("training perceptron")
        rng = np.random.RandomState(42)

        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=0.9, random_state=rng)

        print y_test.size
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)

        yy = []
        #for i in heldout:
        mean = 1 - np.mean(y_pred == y_test)
        num_correct = np.sum(y_pred == y_test)
        '''
        for (p,t) in (y_pred,y_test):
            if p == t:
                print p
                print t
        '''
        print num_correct
        yy.append(mean)

    plt.plot(xx, yy)
        #yy_ = []
        # for r in range(rounds):


            #yy_.append(1 - np.mean(y_pred == y_test))
        #yy.append(np.mean(yy_))



    plt.legend(loc="upper right")
    plt.xlabel("Num Itter")
    plt.ylabel("Test Error Rate")
    # show is broken (and i dont want to deal with setting up the backend, plus having the file is almost better in this case)
    plt.savefig('plots.png')


if __name__=='__main__':
    heldout = [0.5,0.25,0.1,0.01]
    itterations = [range(10,110,10)]
    rounds = 20

    X, y = get_data()
    clf = Perceptron()

    xx = np.array(itterations)

    classify()

    classifiers = [
        #("SGD", SGDClassifier()),
        #("ASGD", SGDClassifier(average=True)),
        ("Perceptron", Perceptron()),
        #("Passive-Aggressive I", PassiveAggressiveClassifier(loss='hinge',
        #                                                     C=1.0)),
        #("Passive-Aggressive II", PassiveAggressiveClassifier(loss='squared_hinge',
        #                                                      C=1.0)),
        #("SAG", LogisticRegression(solver='sag', tol=1e-1, C=1.e4 / X.shape[0]))
    ]
