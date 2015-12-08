from collections import defaultdict
import os
import shutil
import sqlite3
import time
from datetime import datetime
import db_tools
import text_parser
import sentiment_tools
from datetime import datetime

def remove_questions_with_no_acceptedanswer(c):
     cur = c.cursor()

     cur.execute("DELETE FROM questions WHERE acceptedanswerid IS NULL")

     c.commit()

def remove_answers_with_no_question(c):
    cur = c.cursor()

    cur.execute("DELETE FROM answers WHERE pid NOT IN (SELECT id FROM questions)")

    c.commit()

def get_anchor_counts(c):
    db_tools.add_column(c,"answers","links","int")
    db_tools.add_column(c,"questions","links","int")

    # cursor for updating
    cur = c.cursor()
    # cursor for selecting from answers
    a_cur = c.cursor()
    # cursor for selecting from questions
    q_cur = c.cursor()

    q_cur.execute("SELECT id, body FROM questions")
    while True:
        data = q_cur.fetchone()
        if data == None:
            break

        q_id = int(data[0])
        q_body = data[1]
        q_num_links = text_parser.get_anchor_count(q_body)

        cur.execute("UPDATE questions SET links = %i where id = %i" % (q_num_links,q_id))

    c.commit()

    a_cur.execute("SELECT id, body FROM answers")
    while True:
        data = a_cur.fetchone()
        if data == None:
            break

        a_id = int(data[0])
        a_body = data[1]
        a_num_links = text_parser.get_anchor_count(a_body)

        cur.execute("UPDATE answers SET links = %i where id = %i" % (a_num_links,a_id))

    c.commit()

def normalize_text(c):
    db_tools.add_column(c,"answers","links","int")
    db_tools.add_column(c,"questions","links","int")

    # cursor for updating
    cur = c.cursor()
    # cursor for selecting from answers
    a_cur = c.cursor()
    # cursor for selecting from questions
    q_cur = c.cursor()

    q_cur.execute("SELECT id, body, title FROM questions")
    while True:
        data = q_cur.fetchone()
        if data == None:
            break

        q_id = int(data[0])
        q_body = data[1]
        q_title = data[2]
        q_norm_body = text_parser.normalize_text(q_body).encode('ascii','ignore')
        q_norm_title = text_parser.normalize_text(q_title).encode('ascii','ignore')

        cur.execute('UPDATE questions SET body = ? where id = ?',(q_norm_body, q_id))
        cur.execute('UPDATE questions SET title = ? where id = ?',(q_norm_title, q_id))

    c.commit()

    a_cur.execute("SELECT id, body FROM answers")
    while True:
        data = a_cur.fetchone()
        if data == None:
            break

        a_id = int(data[0])
        a_body = data[1]
        a_norm_body = text_parser.normalize_text(a_body).encode('ascii','ignore')

        cur.execute('UPDATE answers SET body = ? where id = ?',(a_norm_body, a_id))

    c.commit()


def mark_accepted_answers(c):
    cur = c.cursor()
    cur.execute("UPDATE answers SET acceptedanswer = 1 WHERE id in (SELECT aaid FROM questions)")
    c.commit()

def analyze_sentiment(c):
    db_tools.add_column(c,"questions","bodysentipolarity","real")
    db_tools.add_column(c,"questions","bodysentisubjectivity","real")
    db_tools.add_column(c,"questions","titlesentipolarity","real")
    db_tools.add_column(c,"questions","titlesentisubjectivity","real")
    db_tools.add_column(c,"answers","bodysentipolarity","real")
    db_tools.add_column(c,"answers","bodysentisubjectivity","real")

    # cursor for updating
    cur = c.cursor()
    # cursor for selecting from answers
    a_cur = c.cursor()
    # cursor for selecting from questions
    q_cur = c.cursor()

    q_cur.execute("SELECT id, body, title FROM questions")
    while True:
        data = q_cur.fetchone()
        if data == None:
            break


        q_id = int(data[0])
        q_body = data[1]
        q_title = data[2]

        q_senti_body_tuple = sentiment_tools.get_sentiment(q_body)
        q_senti_body_polarirty = q_senti_body_tuple[0]
        q_senti_body_subjectivity = q_senti_body_tuple[1]

        cur.execute('UPDATE questions SET bodysentipolarity = ? where id = ?',(q_senti_body_polarirty, q_id))
        cur.execute('UPDATE questions SET bodysentisubjectivity = ? where id = ?',(q_senti_body_subjectivity, q_id))

        q_senti_title_tuple = sentiment_tools.get_sentiment(q_body)
        q_senti_title_polarirty = q_senti_title_tuple[0]
        q_senti_title_subjectivity = q_senti_title_tuple[1]

        cur.execute('UPDATE questions SET titlesentipolarity = ? where id = ?',(q_senti_title_polarirty, q_id))
        cur.execute('UPDATE questions SET titlesentisubjectivity = ? where id = ?',(q_senti_title_subjectivity, q_id))

    c.commit()

    a_cur.execute("SELECT id, body FROM answers")
    while True:
        data = a_cur.fetchone()
        if data == None:
            break

        a_id = int(data[0])
        a_body = data[1]

        a_senti_body_tuple = sentiment_tools.get_sentiment(a_body)
        a_senti_body_polarirty = a_senti_body_tuple[0]
        a_senti_body_subjectivity = a_senti_body_tuple[1]

        cur.execute('UPDATE answers SET bodysentipolarity = ? where id = ?',(a_senti_body_polarirty, a_id))
        cur.execute('UPDATE answers SET bodysentisubjectivity = ? where id = ?',(a_senti_body_subjectivity, a_id))

    c.commit()

def analyze_propmtness_of_answers(c):
    db_tools.add_column(c,"answers","promptness","int")

    # cursor for updating
    cur = c.cursor()
    # cursor for selecting from answers
    a_cur = c.cursor()
    # cursor for selecting from questions
    q_cur = c.cursor()

    a_cur.execute("SELECT id, pid, creationdate FROM answers")
    while True:
        a_data = a_cur.fetchone()
        if a_data == None:
            break

        a_id = int(a_data[0])
        q_id = int(a_data[1])
        a_creationdate = a_data[2]


        q_cur.execute("SELECT creationdate FROM questions WHERE id = %i" % q_id)

        q_data = q_cur.fetchone()
        if q_data == None:
            continue

        q_creationdate = q_data[0]

        promptness = diff_times(a_creationdate,q_creationdate)

        cur.execute("UPDATE answers SET promptness = %i WHERE id = %i" % (promptness,a_id))

    c.commit()


def diff_times(a,q):
    # remove miliseconds
    a = a[:a.rfind('.')]
    q = q[:q.rfind('.')]

    a_time = datetime.strptime(a,"%Y-%m-%dT%H:%M:%S")
    q_time = datetime.strptime(q,"%Y-%m-%dT%H:%M:%S")

    delta_time = a_time - q_time
    return int(delta_time.total_seconds())


if __name__=='__main__':

    db_path = db_tools.get_db_path()
    dt = datetime.now().isoformat()
    bckup_path = db_path+"/bckup/"+dt+/"raw_datadump.db"

    print("Backing up DB to "+bckup_path)
    shutil.copyfile(src, bckup_path)

    # connect to the database
    print("Connecting to DB")
    connection = db_tools.connect()

    print "Removing questions with no acceptedanswer"
    remove_questions_with_no_acceptedanswer(connection)

    print "Removing answers to unstored questions"
    remove_answers_with_no_question(connection)

    print "Getting anchor counts"
    get_anchor_counts(connection)

    print "Normalizing Question and Answer Text"
    normalize_text(connection)

    print "Marking accepted answers"
    mark_accepted_answers(connection)

    print "Analyzing sentiment of Questions and Answers"
    analyze_sentiment(connection)

    print "Analyzing promptness of answers"
    analyze_propmtness_of_answers(connection)

    print "Done, disconnecting from DB"

    connection.close()
