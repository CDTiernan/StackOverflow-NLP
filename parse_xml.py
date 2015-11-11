# import importer as etree
from lxml import etree
import os

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
users = STATIC_PATH+'/datasets/Users.xml'
posts = STATIC_PATH+'/datasets/Posts.xml'

# context = etree.iterparse(infile, events=('end',), tag='DisplayName')
context = etree.iterparse(posts)

def parse_block(elem):
    for key,value in elem.attrib.iteritems():
        print "%s    %s" % (key,value)
    print("")

def fast_iter(context):
    ct = 0
    for event, elem in context:
        if(ct > 100):
            break
        ct += 1

        #print("about to call parse_block")
        print "--------------------- PARSING %i ROW ---------------------" % (ct)
        parse_block(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


fast_iter(context)
