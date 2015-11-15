from lxml import etree
import os
import sqlite3

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
    has_limit = limit is not None

    ct = 0
    for event, elem in context:
        if has_limit:
            if ct > limit:
                break

        if ct % 50000 == 0:
            print "completed %i rows." % (ct)

        populate_questions_answers_tables(elem, c)
        ct += 1

        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]

def create_db(c):
        # connect to db (which creates it)
        cur = c.cursor()

        # create questions table
        cur.execute("CREATE TABLE questions (id int, title string, body string, score int, views int, favorites int, comments int, acceptedanswerid int)")
        # add indecies
        cur.execute("CREATE INDEX qid_idx ON questions(id)")
        cur.execute("CREATE INDEX acceptedanswerid_idx ON questions(acceptedanswerid)")
        # create answers table
        cur.execute("CREATE TABLE answers(id int, body string, score int, commentcount int, pid int, acceptedanswer boolean)")
        # add indecies
        cur.execute("CREATE INDEX aid_idx ON answers(id)");
        cur.execute("CREATE INDEX pid_idx ON answers(pid)");
        cur.execute("CREATE INDEX isacceptedanswer_idx ON answers(acceptedanswer)");

        c.commit()

if __name__=='__main__':
    # DATASET MUST BE IN SOURCE FOLDER WITHIN A FOLDER CALLED 'datasets'
    static_path = os.getcwd()
    users = static_path+'/datasets/Users.xml'
    posts = static_path+'/datasets/Posts.xml'

    # check to see if database exists
    have_db = os.path.isfile('db/datadump.db')

    # connect to the dataset
    context = etree.iterparse(posts)
    # connect to the database (and create it)
    connection = sqlite3.connect('db/datadump.db')

    # if db does not exist
    if not have_db:
        print("Creating and Connecting to DB")
        create_db(connection)
    else:
        print("Connecting to DB")

    print("Populating DB")
    fast_iter(context, connection, limit=1000)

    connection.close()
    del context
