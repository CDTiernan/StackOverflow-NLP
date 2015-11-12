# import importer as etree
from lxml import etree
import os
from collections import defaultdict
import pprint

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
users = STATIC_PATH+'/datasets/Users.xml'
posts = STATIC_PATH+'/datasets/Posts.xml'

# context = etree.iterparse(infile, events=('end',), tag='DisplayName')
context = etree.iterparse(posts)

def get_question(elem, d):
    is_question = elem.attrib['PostTypeId'] is "1"
    if is_question:
        id = elem.attrib['Id']
        d[id] = 1
        
def get_answer(elem, d):
    is_answer = elem.attrib['PostTypeId'] is "2"
    if is_answer:
        for question in d.iteritems():
            if question is elem.attrib['ParentId']:
                print("adding answer")
                # current elem is answer to this question
                answer_id = elem.attrib['Id']
                d[question][answer_id] = elem.attrib
            
        
    # for key,value in elem.attrib.iteritems():
        # print "%s    %s" % (key,value)

def fast_iter(context, func, d, limit=None):
    ct = 0
    has_limit = limit is not None
    
    for event, elem in context:
        if has_limit:
            if ct > limit:
                break
        ct += 1

        # print "--------------------- PARSING %i ROW ---------------------" % (ct)
        func(elem, d)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    return d



questions_dict = defaultdict(int)
print("getting questions...")
fast_iter(context, get_question, questions_dict, limit=10)
print("number of questions: %d" % len(questions_dict))


print("getting answers...")
fast_iter(context, get_answer, questions_dict)

    
print("")
pprint.pprint(questions_dict)
