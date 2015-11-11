from lxml import etree

# PATH MUST BE CHANGED for each users
infile = '/Users/Matt/Desktop/stackexchange/Users.xml'
context = etree.iterparse(infile, events=('end',), tag='Title')

ct = 0

fast_iter(context, parse_block)

def parse_block(elem):
    print("count is %d" % ct)
    print(elem)
    print("")
    ct += 1

def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
