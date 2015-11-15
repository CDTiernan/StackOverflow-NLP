# import importer as etree
from lxml import etree
import os
from collections import defaultdict
import pprint
import pickle
import sqlite3
import unicodedata

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
users = STATIC_PATH+'/datasets/Users.xml'
posts = STATIC_PATH+'/datasets/Posts.xml'

def get_question(elem, c):
    is_question = elem.attrib['PostTypeId'] is "1"
    has_accepted_answer = 'AcceptedAnswerId' in elem.attrib

    if is_question and has_accepted_answer:
        q_id = int(elem.attrib['Id'])
        # tilte unicodedata.normalize('NFKD', elem.attrib['Title']).encode('ascii','ignore')
        title = elem.attrib['Title'].encode('ascii','ignore')
        # tilte unicodedata.normalize('NFKD', elem.attrib['Body']).encode('ascii','ignore')
        body = elem.attrib['Body'].encode('ascii','ignore')
        score = int(elem.attrib['Score'])
        views = int(elem.attrib['ViewCount'])
        accepted_answer_id = int(elem.attrib['AcceptedAnswerId'])

        q_cur = c.cursor()

        q_cur.execute('INSERT INTO questions (id, title, body, score, views, acceptedanswerid) VALUES (?, ?, ?, ?, ?, ?)', (q_id, title, body, score, views, accepted_answer_id))
        #q_cur.execute("INSERT INTO questions (id, title, body, score, views, acceptedanswerid) VALUES (%i, %s, %s, %i, %i, %i)" % (q_id, title, body, score, views, accepted_answer_id))
        c.commit()

        '''
        d[q_id]["title"] = accepted_answer_id
        d[q_id]["body"] = body
        d[q_id]["score"] = score
        d[q_id]["views"] = views
        d[q_id]["accepted_answer_id"] = accepted_answer_id
        d[q_id]["answers_ids"] = []
        '''

def get_answer(elem, c):
    is_answer = elem.attrib['PostTypeId'] is "2"

    if is_answer:
        a_id = int(elem.attrib['Id'])
        body = str(elem.attrib['Body']).encode('ascii','ignore')
        score = int(elem.attrib['Score'])
        q_id = int(elem.attrib['ParentId'])


        a_cur = c.cursor()

        a_cur.execute('INSERT INTO answers (id, body, score, pid) VALUES (?, ?, ?, ?)', (a_id, body, score, q_id))
        c.commit()


        '''
        d[a_id]["body"] = body
        d[a_id]["score"] = score
        d[a_id]["parent_id"] = q_id
        '''
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

        q_cur.execute('INSERT INTO questions (id, title, body, score, views, acceptedanswerid) VALUES (?, ?, ?, ?, ?, ?)', (q_id, title, body, score, views, accepted_answer_id))
        c.commit()


    is_answer = elem.attrib['PostTypeId'] is "2"
    if is_answer:
        a_id = int(elem.attrib['Id'])
        body = elem.attrib['Body'].encode('ascii','ignore')
        score = int(elem.attrib['Score'])
        q_id = int(elem.attrib['ParentId'])

        a_cur = c.cursor()

        a_cur.execute('INSERT INTO answers (id, body, score, pid) VALUES (?, ?, ?, ?)', (a_id, body, score, q_id))
        c.commit()

def fast_iter(context, c, limit=None):
    ct = 0
    has_limit = limit is not None

    for event, elem in context:
        if has_limit:
            if ct > limit:
                break
        if ct % 50000 == 0:
            print "completed %i rows." % (ct)
        # func(elem,c)
        populate_questions_answers_tables(elem, c)
        ct += 1

        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
'''
def link_dicts(qd,ad):
    answers_with_no_question = []
    for a_id,info_dict in ad.iteritems():
        q_id = info_dict["parent_id"]
        if q_id in qd:
            qd[q_id]["answers_ids"].append(a_id)
            if qd[q_id]["accepted_answer_id"] == a_id:
                ad[a_id]["is_accepted"] = 1
        else:
            answers_with_no_question.append(a_id)

    return answers_with_no_question

def delete_unused_answers(td,ad):
    for a_id in td:
        del ad[a_id]
'''

context = etree.iterparse(posts)

'''
def dd():
    return defaultdict(int)
questions_dict = defaultdict(dd) # dd is a module-level function
answers_dict = defaultdict(dd) # dd is a module-level function
'''
conn = sqlite3.connect('db/datadump.db')

print("populating questions and answers...")
fast_iter(context, conn, limit=None)
# fast_iter(context, get_question, questions_dict, limit=None)
# print("number of questions: %d" % len(questions_dict))

# print("getting answers...")
# fast_iter(context, get_answer,  conn, limit=None)

# cur = c.cursor()
# cur.execute('SELECT count(id) from questions')

# fast_iter(context, get_answer, answers_dict, limit=None)
# print("number of answers pre-deleting unused: %d" % len(answers_dict))

# to_del = link_dicts(questions_dict,answers_dict)
# delete_unused_answers(to_del,answers_dict)
# print("number of post-answers unused: %d" % len(answers_dict))

# pickle.dump( questions_dict, open( "questions.p", "wb" ) )
# pickle.dump( answers_dict, open( "answers.p", "wb" ) )

# print("")
# pprint.pprint(questions_dict)

conn.close()
