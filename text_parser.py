import nltk
from nltk.tokenize import StanfordTokenizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import WordPunctTokenizer
import re

def remove_code_samples(text):
    return re.sub("<code>[a-zA-Z.]*</code> ",'',text)

def remove_html_elements(text):
    return re.sub("<+/*[a-zA-Z0-9]*>",'',text)

def tokenize_white_space(text):
    return WhitespaceTokenizer().tokenize(text)

def tokenize_white_space_punct(text):
    return WordPunctTokenizer().tokenize(text)

def tokenize_word(text):
    return nltk.word_tokenize(text)

def tokenize_stanford(text):
    return StanfordTokenizer().tokenize(text)
