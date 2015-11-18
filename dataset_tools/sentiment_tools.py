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
Returns True if sentiment of text is positive
Since polarity ranges from 0 to 1, it is postive if the polarity is greater than 0.5
'''
def is_sentiment_positive(text):
    return get_sentiment_polarity(text) > 0.5

'''
Returns polarity of text between 0 and 1
0 is most negative
1 is most positive
'''
def get_sentiment_polarity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

'''
Returns sentiment of text as a namedtuple of the form Sentiment(polarity, subjectivity)
'''
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment



if __name__=='__main__':
    pos = get_sentiment_polarity("that answer is perfect. Worked flawlessly")
    neg = get_sentiment_polarity("I'm horrified that you would recommend that course of action")
    print("polarity of positive string: %f" % pos)
    print("polarity of negative string: %f" % neg)
