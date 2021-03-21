import string

from nltk.corpus import stopwords
from utils import *

def exclude_numeric(tokens):
    num = [str(i) for i in range(10)]
    return set([token for token in tokens if all(not j in num for j in token)])

def exclude_stop_words(tokens):
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', 'o'])
    stop_words.extend(stopwords.words('english'))
    return set([token for token in tokens if token not in stop_words])

def exclude_punctuation(tokens):
    return set([token for token in tokens if all(not j in string.punctuation for j in token)])

def exclude_trash(tokens):
    trash = ['«', '»', '→', '·', '®', '▼', '–', '▸', 'x', 'X', '𗼇']
    return set([token for token in tokens if token not in trash])

def exclude_not_russion_or_english(tokens):
    return set([token for token in tokens if (is_cyrillic(token) or is_english(token))])

def filter_tokens(tokens):
    tokens = exclude_stop_words(tokens)
    tokens = exclude_punctuation(tokens)
    tokens = exclude_trash(tokens)
    tokens = exclude_numeric(tokens)
    tokens = split_camel_case(tokens)
    tokens = exclude_not_russion_or_english(tokens)
    return tokens