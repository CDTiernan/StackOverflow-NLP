import db_tools
import text_parser
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


if __name__=='__main__':
    print("Connecting to DB")
    connection = db_tools.connect()

    cur = connection.cursor()

    cur.execute("SELECT body FROM answers")

    while True:
        data = cur.fetchone()
        if data == None:
            break

        body = data[0]

        no_code = text_parser.remove_code_samples(body)
        #strip = striphtml(no_code)

        print body
