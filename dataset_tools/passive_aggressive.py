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

    connection = db_tools.connect()
    cur = connection.cursor()

    # get number of rows so training array can be built
    cur.execute("SELECT count(id) FROM answers")

    data = cur.fetchone()
    num_rows = data[0]

    build_X = np.ndarray(shape=(num_rows,x_feats), dtype=float, order='C')
    build_y = np.ndarray(shape=(num_rows,), dtype=float, order='C')

    # get all data necessary to train
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
    for name, clf in classifiers:
        print("training %s" % name)
        rng = np.random.RandomState(42)
        yy = []
        for i in heldout:
            yy_ = []
            yy__ = []
            for r in range(1):
                X_train, X_test, y_train, y_test = \
                    train_test_split(X, y, test_size=i, random_state=rng)
                clf.fit(X_train, y_train)
                y_pred = clf.predict(X_test)
                yy_.append(1 - np.mean(y_pred == y_test))
                nright = np.sum(y_pred == y_test)
                nwrong = np.sum(y_pred != y_test)
                pright = float(nright/float(nright + nwrong))
                yy__.append(pright*100)

                j = 0
                counts = {'fp':0,'tp':0,'fn':0,'tn':0}
                for pred in y_pred:
                    if y_pred[j] == 1 and y_test[j] == 0:
                        counts['fp'] += 1
                    elif y_pred[j] == 1 and y_test[j] == 1:
                        counts['tp'] += 1
                    elif y_pred[j] == 0 and y_test[j] == 1:
                        counts['fn'] += 1
                    elif y_pred[j] == 0 and y_test[j] == 0:
                        counts['tn'] += 1
                    j += 1

                print i
                print counts

            yy.append(np.mean(yy__))
        plt.plot(xx, yy, label=name)

    plt.legend(loc="best")
    plt.xlabel("Proportion train")
    plt.ylabel("Prec Right")
    # show is broken (and i dont want to deal with setting up the backend, plus having the file is almost better in this case)
    plt.savefig('multplots.png')


if __name__=='__main__':
    heldout = [0.7,0.6,0.5,0.4,0.3,0.2,0.1]
    itterations = [range(10,110,10)]
    rounds = 20

    X, y = get_data()

    xx = 1.0 - np.array(heldout)

    classifiers = [
        ("Passive-Aggressive I", PassiveAggressiveClassifier(loss='squared_hinge',
                                                             warm_start=True,
                                                             fit_intercept=True,
                                                             C=1.0)),
        ("Passive-Aggressive II", PassiveAggressiveClassifier(loss='hinge',
                                                             fit_intercept=True,
                                                             n_iter = 10,
                                                             C=1.0)),
        ("Passive-Aggressive III", PassiveAggressiveClassifier(loss='hinge',
                                                             fit_intercept=True,
                                                             n_iter = 20,
                                                             C=1.0)),
        ("Passive-Aggressive IV", PassiveAggressiveClassifier(loss='hinge',
                                                             fit_intercept=True,
                                                             n_iter = 50,
                                                             C=1.0)),
        ("Passive-Aggressive V", PassiveAggressiveClassifier(loss='hinge',
                                                             fit_intercept=True,
                                                             n_iter = 100,
                                                             C=1.0)),
        ("Passive-Aggressive VI", PassiveAggressiveClassifier(loss='hinge',
                                                             fit_intercept=True,
                                                             C=1.0))
    ]


    classify()
