from lxml import etree
import os
import sqlite3
import db_tools

def populate_questions_answers_tables(elem, c):

    is_question = elem.attrib['PostTypeId'] is "1"
    has_accepted_answer = 'AcceptedAnswerId' in elem.attrib
    if is_question and has_accepted_answer:
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
        a_id = int(elem.attrib['Id'])
        body = elem.attrib['Body'].encode('ascii','ignore')
        score = int(elem.attrib['Score'])
        q_id = int(elem.attrib['ParentId'])

        a_cur = c.cursor()
        a_cur.execute('INSERT OR IGNORE INTO answers (id, body, score, pid) VALUES (?, ?, ?, ?)', (a_id, body, score, q_id))
        c.commit()

def fast_iter(context, c, limit=None):
    has_limit = limit is not None

    ct = 0
    for event, elem in context:
        if has_limit:
            if ct > limit:
                break

        if ct % 50000 == 0:
            print("completed %i rows." % (ct))

        populate_questions_answers_tables(elem, c)
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



    print("Populating DB")
    fast_iter(context, connection, limit=10000)

    connection.close()
    del context
