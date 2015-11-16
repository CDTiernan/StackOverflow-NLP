from textblob import TextBlob

'''
textblob library needs to be installed for this to work
to install, run the two commands below separately:

pip install textblob
python -m textblob.download_corpora


link to tutorial:
https://textblob.readthedocs.org/en/dev/quickstart.html#sentiment-analysis
'''




'''
returns polarity of text between 0 and 1
0 is most negative
1 is most positive
'''
def get_sentiment_polarity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


if __name__=='__main__':
    pos = get_sentiment_polarity("that answer is perfect. Worked flawlessly")
    neg = get_sentiment_polarity("I'm horrified that you would recommend that course of action")
    print(pos)
    print(neg)
