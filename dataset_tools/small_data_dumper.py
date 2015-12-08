from lxml import etree
from collections import defaultdict
import os
import sqlite3
import db_tools




def build_id_dict():
    ids = [961942, 61088, 885009, 1644, 133556, 245395, 83073, 146297, 180939, 811074,
        3088, 41479, 121243, 500607, 3538156, 61401, 686216, 188162, 2767, 161872, 169713,
        111102, 54886, 901115, 521893, 278526, 164847, 137783, 1840847, 157354, 726894,
        14155, 652788, 2388254, 201323, 52002, 1124968, 2680827, 490420, 106340, 514083,
        513953, 102084, 75538, 350885, 236129, 162144, 2757107, 241134, 1554099]

    tmpDict = defaultdict(float)
    for id in ids:
        tmpDict[id] = []

    return tmpDict


def populate_questions_answers_tables(elem, c, qIds):

    try:
        is_question = elem.attrib['PostTypeId'] is "1"
        has_accepted_answer = 'AcceptedAnswerId' in elem.attrib
        in_question_set = int(elem.attrib['Id']) in qIds

        if in_question_set and is_question and has_accepted_answer:
            q_id = int(elem.attrib['Id'])
            title = elem.attrib['Title'].encode('ascii','ignore')
            body = elem.attrib['Body'].encode('ascii','ignore')
            score = int(elem.attrib['Score'])
            views = int(elem.attrib['ViewCount'])
            accepted_answer_id = int(elem.attrib['AcceptedAnswerId'])

            q_cur = c.cursor()
            q_cur.execute('INSERT OR IGNORE INTO questions (id, title, body, score, views, acceptedanswerid) VALUES (?, ?, ?, ?, ?, ?)', (q_id, title, body, score, views, accepted_answer_id))
            c.commit()

        is_answer = elem.attrib['PostTypeId'] is "2"

        if is_answer:
            is_answer_for_question_set = int(elem.attrib['ParentId']) in qIds

            if is_answer_for_question_set:
                a_id = int(elem.attrib['Id'])
                body = elem.attrib['Body'].encode('ascii','ignore')
                score = int(elem.attrib['Score'])
                q_id = int(elem.attrib['ParentId'])

                qIds[q_id].append(a_id)

                a_cur = c.cursor()
                a_cur.execute('INSERT OR IGNORE INTO answers (id, body, score, pid) VALUES (?, ?, ?, ?)', (a_id, body, score, q_id))
                c.commit()
    except Exception:
        print "SKIPPING POST: Lazy handling of error in which some posts dont have PostTypeId."
        pass

def fast_iter(context, c, qIds,limit):
    has_limit = limit is not None

    ct = 0
    for event, elem in context:
        if has_limit:
            if ct > limit:
                break

        if ct % 50000 == 0:
            print("completed %i rows." % (ct))

        populate_questions_answers_tables(elem, c, qIds)
        ct += 1

        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]

if __name__=='__main__':
    # DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
    static_path = os.getcwd()
    users = static_path+'/../datasets/Users.xml'
    posts = static_path+'/../datasets/Posts.xml'

    # connect to the dataset
    context = etree.iterparse(posts)

    # connect to the database
    print("Connecting to DB")
    connection = db_tools.get_connection()


    # questions we will be looking at will be initialized to have an empty array
    # everything else is unititialized, therefore returning 0.0
    questionIds = build_id_dict()


    n = 50
    print("Putting %i questions in DB" % (n))
    fast_iter(context, connection, questionIds, limit = None)

    print questionIds

    connection.close()
    del context
