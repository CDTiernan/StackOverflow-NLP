# import importer as etree
from lxml import etree
import os

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
infile = STATIC_PATH+'/datasets/Users.xml'

# context = etree.iterparse(infile, events=('end',), tag='DisplayName')
context = etree.iterparse(infile)

def parse_block(elem):
    for key,value in elem.attrib.iteritems():
        print "%s    %s" % (key,value)
    print("")

def fast_iter(context):
    ct = 0
    for event, elem in context:
        if(ct > 10):
            break
        ct += 1

<<<<<<< HEAD
        #print("about to call parse_block")
        print "--------------------- PARSING %i ROW ---------------------" % (ct)
=======
>>>>>>> c6c1d4c4e64e90bc5d194b1a5f903900bc729337
        parse_block(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


fast_iter(context)
