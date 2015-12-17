from lxml import etree
from collections import defaultdict
import os
import sys
import sqlite3
import db_tools

def build_id_dict(size):
    # Ids where selected from some of the top most answered questions to get more anser data
    if size == "small":
        ids = [961942, 61088, 885009, 1644, 133556, 245395, 83073, 146297, 180939, 811074,
            3088, 41479, 121243, 500607, 3538156, 61401, 686216, 188162, 2767, 161872, 169713,
            111102, 54886, 901115, 521893, 278526, 164847, 137783, 1840847, 157354, 726894,
            14155, 652788, 2388254, 201323, 52002, 1124968, 2680827, 490420, 106340, 514083,
            513953, 102084, 75538, 350885, 236129, 162144, 2757107, 241134, 1554099
        ]
    elif size == "med":
        ids = [961942, 61088, 885009, 1644, 133556, 245395, 83073, 146297, 180939, 811074,
            3088, 41479, 121243, 500607, 3538156, 61401, 686216, 188162, 2767, 161872, 169713,
            111102, 54886, 901115, 521893, 278526, 164847, 137783, 1840847, 157354, 726894,
            14155, 652788, 2388254, 201323, 52002, 1124968, 2680827, 490420, 106340, 514083,
            513953, 102084, 75538, 350885, 236129, 162144, 2757107, 241134, 1554099,
            8021370, 8741865, 11578671, 14436804, 11926489, 3318735, 4223623, 7658650,
            6213178, 3690067, 12692067, 6146973, 4860685, 17544303, 22272800, 17006625,
            2638099, 10757101, 18952958, 5133227, 28406952, 5163493, 3876194, 12291038,
            1069433, 1334299, 13859384, 2448244, 4018050, 3475274, 6372096, 1964008, 9067015,
            3475148, 4582435, 33697942, 4559221, 5094915, 10892743, 31980966, 9380295,
            7421687, 18100067, 6450869, 10338524, 26214428, 6728329, 2398588, 9230567,
            31188378, 5854965, 22250652, 419900, 17691265, 2996139, 12617408, 7855436,
            10919092, 5813898, 9332573, 5767274, 10620078, 7857984, 7318968, 12406983,
            9817542, 10783283, 6252333, 7497302, 11281141, 8396405, 5231351, 5388212,
            11589207, 18022929, 11221339, 5101216, 6602030, 6699225, 12566763, 12373347,
            9213523, 31375665, 7729868, 2146944, 11055232, 5279791, 7663584, 5510253, 7724357,
            33447061, 8551762, 8784529, 7714429, 6119968, 10047584, 2462071, 5144060, 28119872,
            9713637
        ]

    # Put question ids into dict so its efficient to check if what we are parsing is something to store
    tmpDict = defaultdict(float)
    for id in ids:
        tmpDict[id] = []

    return tmpDict


def populate_questions_answers_tables(elem, c, qIds):

    # errors shouldnt ruin db (and lazy handling of key errors like no elem.attrib['PostTypeId'])
    #try:

        if 'PostTypeId' in elem.attrib:
            is_question = elem.attrib['PostTypeId'] is "1"
            has_accepted_answer = 'AcceptedAnswerId' in elem.attrib
            in_question_set = int(elem.attrib['Id']) in qIds

            # if this question should be stored add it to db
            if in_question_set and is_question and has_accepted_answer:
                q_id = int(elem.attrib['Id'])
                title = elem.attrib['Title'].encode('ascii','ignore')
                body = elem.attrib['Body'].encode('ascii','ignore')
                score = int(elem.attrib['Score'])
                if 'ViewCount' in elem.attrib:
                    viewcount = int(elem.attrib['ViewCount'])
                else:
                    viewcount = 0

                if 'FavoriteCount' in elem.attrib:
                    favcount = int(elem.attrib['FavoriteCount'])
                else:
                    favcount = 0

                if 'CommentCount' in elem.attrib:
                    commcount = int(elem.attrib['CommentCount'])
                else:
                    commcount = 0
                aaid = int(elem.attrib['AcceptedAnswerId'])

                if 'AnswerCount' in elem.attrib:
                    answercount = int(elem.attrib['AnswerCount'])
                else:
                    answercount = 0
                creationdate = elem.attrib['CreationDate'].encode('ascii','ignore')
                lastactivitydate =elem.attrib['LastActivityDate'].encode('ascii','ignore')
                tags = elem.attrib['Tags'].encode('ascii','ignore')


                q_cur = c.cursor()
                q_cur.execute('INSERT OR IGNORE INTO questions (id, title, body, score, viewcount, favcount, commcount, aaid, answercount, creationdate, lastactivitydate, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (q_id, title, body, score, viewcount, favcount, commcount, aaid, answercount, creationdate, lastactivitydate, tags))
                c.commit()

            is_answer = elem.attrib['PostTypeId'] is "2"

            # if this answer should be stored add it to db
            if is_answer:
                is_answer_for_question_set = int(elem.attrib['ParentId']) in qIds
                if is_answer_for_question_set:
                    a_id = int(elem.attrib['Id'])
                    body = elem.attrib['Body'].encode('ascii','ignore')
                    score = int(elem.attrib['Score'])
                    if 'CommentCount' in elem.attrib:
                        commcount = int(elem.attrib['CommentCount'])
                    else:
                        commcount = 0
                    q_id = int(elem.attrib['ParentId'])
                    creationdate = elem.attrib['CreationDate'].encode('ascii','ignore')
                    lastactivitydate = elem.attrib['LastActivityDate'].encode('ascii','ignore')

                    qIds[q_id].append(a_id)

                    a_cur = c.cursor()
                    a_cur.execute('INSERT OR IGNORE INTO answers (id, body, score, commcount, pid, creationdate, lastactivitydate) VALUES (?, ?, ?, ?, ?, ?, ?)', (a_id, body, score, commcount, q_id, creationdate, lastactivitydate))
                    c.commit()
    #except:
    #    print elem.attrib
    #    e = sys.exc_info()[0]
    #    print "%s" % e # "SKIPPING POST: Lazy handling of error in which some posts dont have PostTypeId."
    #    pass

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
    connection = db_tools.connect()
    print("Setting up DB (if necessary)")
    db_tools.setup_db(connection)


    # questions we will be looking at will be initialized to have an empty array
    # everything else is unititialized, therefore returning 0.0
    questionIds = build_id_dict('med')


    print("Populating DB")
    fast_iter(context, connection, questionIds, limit = None)

    connection.close()
    del context
