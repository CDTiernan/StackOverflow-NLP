# import importer as etree
from lxml import etree
import os
from collections import defaultdict
import pprint
import pickle

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
users = STATIC_PATH+'/datasets/Users.xml'
posts = STATIC_PATH+'/datasets/Posts.xml'

def get_question(elem, d):
    is_question = elem.attrib['PostTypeId'] is "1"
    has_accepted_answer = 'AcceptedAnswerId' in elem.attrib

    if is_question and has_accepted_answer:
        q_id = elem.attrib['Id']
        title = elem.attrib['Title']
        body = elem.attrib['Body']
        score = elem.attrib['Score']
        views = elem.attrib['ViewCount']
        accepted_answer_id = elem.attrib['AcceptedAnswerId']

        d[q_id]["title"] = accepted_answer_id
        d[q_id]["body"] = body
        d[q_id]["score"] = score
        d[q_id]["views"] = views
        d[q_id]["accepted_answer_id"] = accepted_answer_id
        d[q_id]["answers_ids"] = []

def get_answer(elem, d):
    is_answer = elem.attrib['PostTypeId'] is "2"

    if is_answer:
        a_id = elem.attrib['Id']
        body = elem.attrib['Body']
        score = elem.attrib['Score']
        q_id = elem.attrib['ParentId']

        d[a_id]["body"] = body
        d[a_id]["score"] = score
        d[a_id]["parent_id"] = q_id
    '''
    is_answer = elem.attrib['PostTypeId'] is "2"
    if is_answer:
        q_id = elem.attrib['ParentId']
        #print q_id
        is_answer_to_question = q_id in d
        if is_answer_to_question:
            a_id = elem.attrib['Id']
            d[q_id]["answers_ids"].append(a_id)


        for question in d.iteritems():
            if question is elem.attrib['ParentId']:
                print("adding answer")
                # current elem is answer to this question
                answer_id = elem.attrib['Id']
                d[question][answer_id] = elem.attrib
                break
        '''

def fast_iter(context, func, d, limit=None):
    ct = 0
    has_limit = limit is not None

    for event, elem in context:
        if has_limit:
            if ct > limit:
                break
        ct += 1
        #print ct
        func(elem, d)
        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

def link_dicts(qd,ad):
    for a_id,info_dict in ad.iteritems():
        q_id = info_dict["parent_id"]
        if q_id in qd:
            qd[q_id]["answers_ids"].append(a_id)
            if qd[q_id]["accepted_answer_id"] == a_id:
                ad[a_id]["is_accepted"] = 1

context = etree.iterparse(posts)

def dd():
    return defaultdict(int)
questions_dict = defaultdict(dd) # dd is a module-level function
answers_dict = defaultdict(dd) # dd is a module-level function

print("getting questions...")
fast_iter(context, get_question, questions_dict, limit=1000000)
print("number of questions: %d" % len(questions_dict))

print("getting answers...")
fast_iter(context, get_answer, answers_dict, limit=1000000)
print("number of answers: %d" % len(answers_dict))

link_dicts(questions_dict,answers_dict)

pickle.dump( questions_dict, open( "questions.p", "wb" ) )
pickle.dump( answers_dict, open( "answers.p", "wb" ) )

# print("")
# pprint.pprint(questions_dict)
