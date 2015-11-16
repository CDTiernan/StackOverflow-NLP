from textblob import TextBlob

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
