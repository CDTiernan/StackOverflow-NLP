# import importer as etree
from lxml import etree

# PATH MUST BE CHANGED for each users
infile = '/Users/Matt/Desktop/stackexchange/Users.xml'
# context = etree.iterparse(infile, events=('end',), tag='DisplayName')
context = etree.iterparse(infile)
ct = 0



def parse_block(elem):
    print("printing elem")
    print(elem.tag)
    print elem.tag, elem.attrib['DownVotes']
    for thing in elem:
        print(thing)
    print("")

def fast_iter(context):
    ct = 0
    print("starting fast iterator")
    print("printing context...")
    print(context)
    for event, elem in context: 
        if(ct > 10):
            break
        print("count is %d" % ct)
        ct += 1
        
        print("about to call parse_block")       
        parse_block(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


fast_iter(context)
