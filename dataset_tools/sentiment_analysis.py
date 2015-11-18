import sqlite3
import text_parser

if __name__=='__main__':
    connection = sqlite3.connect('db/datadump.db')

    cur = connection.cursor()
    cur.execute("SELECT body FROM answers where pid=4")

    for i in range(10):
        body = cur.next()[0]

        no_html = text_parser.remove_html_elements(body)
        no_html_code = text_parser.remove_code_samples(no_html)

        print text_parser.tokenize_stanford(no_html_code)

    connection.commit()
    connection.close()
