# import importer as etree
from lxml import etree
import os
from collections import defaultdict

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
users = STATIC_PATH+'/datasets/Users.xml'
posts = STATIC_PATH+'/datasets/Posts.xml'

# context = etree.iterparse(infile, events=('end',), tag='DisplayName')
context = etree.iterparse(posts)

def parse_block(elem, d):
    isQuestion = elem.attrib['PostTypeId'] == "1"
    if isQuestion:
        id = elem.attrib['Id']
        d[id] = 1
        
    # for key,value in elem.attrib.iteritems():
        # print "%s    %s" % (key,value)

def fast_iter(context):
    ct = 0
    d = defaultdict(lambda: defaultdict(int))
    
    for event, elem in context:
        # if(ct > 10000):
            # break
        ct += 1
        if ct % 1000000 == 0:
            print("at ct: %d" % ct)

        # print "--------------------- PARSING %i ROW ---------------------" % (ct)
        parse_block(elem, d)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    return d

questions_dict = fast_iter(context)
for question_id in questions_dict.iteritems():
    print(question_id)
    
print("")
print("number of questions: %d" % len(questions_dict))
