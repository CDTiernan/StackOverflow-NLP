# import importer as etree
from lxml import etree
import os

# DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
STATIC_PATH = os.getcwd()
infile = STATIC_PATH+'/datasets/Users.xml'

# context = etree.iterparse(infile, events=('end',), tag='DisplayName')
context = etree.iterparse(infile)
ct = 0



def parse_block(elem):
    print(elem)
    print("")

def fast_iter(context):
    ct = 0
    print("starting fast iterator")
    print("printing context...")
    print(context)
    for event, elem in context:
        print("count is %d" % ct)
        ct += 1
        print("about to call parse_block")
        parse_block(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


fast_iter(context)
