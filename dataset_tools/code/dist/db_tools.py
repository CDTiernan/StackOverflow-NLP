import sqlite3
import os

''' STATIC PATH FOR DATABASE '''
DATABASE_PATH = '../db/datadump.db'
DATABASE_DIRECTORY = os.getcwd()+'/db'

'''
Creates db tables and indices if they don't exist,
then returns connection to db
'''
def get_connection():
    return setup_db()

'''
Returns connection to database
'''
def connect():
    # create db folder if there isn't one already
    if not os.path.exists(DATABASE_DIRECTORY):
        os.makedirs(DATABASE_DIRECTORY)

    # connect to db (which creates it)
    return sqlite3.connect(DATABASE_PATH)

'''
Check database and creates any parts that don't exists
 * Creates folder for database if it doesn't exist
 * Creates database if it doesn't exist
 * Creates questions table if it doesn't exist
 * Creates indices for questions table if they don't exist
 * Creates answers table if it doesn't exist
 * Creates indices for answers table if they don't exist
'''
def setup_db(conn):
    cur = conn.cursor()

    # QUESTIONS TABLE
    # create questions table if it's not there
    cur.execute("CREATE TABLE IF NOT EXISTS questions (" +
                "id int, " +
                "title string, " +
                "body string, " +
                "score int, " +
                "viewcount int, " +
                "favcount int, " +
                "commcount int, " +
                "aaid int, " +
                "answercount int, " +
                "creationdate string, " +
                "lastactivitydate string, " +
                "tags string, " +
                "PRIMARY KEY (id))")
    # add indices if they aren't there
    cur.execute("CREATE INDEX IF NOT EXISTS qid_idx ON questions(id)")
    cur.execute("CREATE INDEX IF NOT EXISTS acceptedanswerid_idx ON questions(aaid)")

    # ANSWERS TABLE
    # create answers table if it's not there
    cur.execute("CREATE TABLE IF NOT EXISTS answers (" +
                "id int, " +
                "body string, " +
                "score int, " +
                "commcount int, " +
                "pid int, " +
                "acceptedanswer boolean, " +
                "creationdate string," +
                "lastactivitydate string," +
                "PRIMARY KEY (id))")
    # add indices if they aren't there
    cur.execute("CREATE INDEX IF NOT EXISTS aid_idx ON answers(id)");
    cur.execute("CREATE INDEX IF NOT EXISTS pid_idx ON answers(pid)");
    cur.execute("CREATE INDEX IF NOT EXISTS isacceptedanswer_idx ON answers(acceptedanswer)");

    conn.commit()
    return conn

def add_column(conn,table,colName,colType):
    cur = conn.cursor()
    try:
        cur.execute("SELECT "+colName+" from "+table)
    except Exception:
        cur.execute("ALTER TABLE "+table+" ADD COLUMN "+colName+" "+colType)

def get_db_path():
    path = DATABASE_PATH[:DATABASE_PATH.rfind('/')]
    return path

if __name__=='__main__':
    conn = get_connection()
    conn.close()
