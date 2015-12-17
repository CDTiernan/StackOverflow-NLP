import nltk
#from nltk.tokenize import StanfordTokenizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import WordPunctTokenizer
import re


def normalize_text(text):
    if len(text) > 0:
        no_code = remove_code_samples(text)
        no_code_anchor = remove_anchors(no_code)
        no_code_anchor_html = remove_html_elements(no_code_anchor)
    else:
        no_code_anchor_html = text

    return no_code_anchor_html


#def get_code_sample_count(text):
#    return text.count('<code')

def get_anchor_count(text):
    return text.count('<a ')


def remove_code_samples(text):
    return re.sub("<code>[a-zA-Z.]*</code> ",'',text)

#needs work
def remove_anchors(text):
    return re.sub("<a.*>.*</a> ",'',text)



def remove_html_elements(text):
    return re.sub("<+/*[a-zA-Z0-9]*>",'',text)

def tokenize_white_space(text):
    return WhitespaceTokenizer().tokenize(text)

def tokenize_white_space_punct(text):
    return WordPunctTokenizer().tokenize(text)

def tokenize_word(text):
    return nltk.word_tokenize(text)

#def tokenize_stanford(text):
    #return StanfordTokenizer().tokenize(text)
