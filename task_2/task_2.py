import zipfile
import nltk
import string
import pymorphy2

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from utils import camel_case_split

def split_camel_case(tokens):
    splited = []
    added = []

    for token in tokens:
        words = camel_case_split(token)
        if len(words) > 0:
            splited.append(token)
            added.extend(words)

    tokens -= set(splited)
    tokens |= set(added)
    return tokens

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

def lemmatization(tokenization_result):
    morph = pymorphy2.MorphAnalyzer()
    lemmatization_map = dict()
    for word in tokenization_result:
        try:
            p = morph.parse(word)[0]
            if p.normalized.is_known:
                normal_form = p.normal_form
            else:
                normal_form = word.lower()
            if not normal_form in lemmatization_map:
                lemmatization_map[normal_form] = []
            lemmatization_map[normal_form].append(word)
        except Exception:
            continue
    return lemmatization_map

def write_lemmatization_result(lemmatization_result):
    with open("lemmatization.txt", "w") as file:
        for lemma, tokens in lemmatization_result.items():
            file_string = lemma + " "
            for token in tokens:
                file_string += token + " "
            file_string += "\n"
            file.write(file_string)

def write_tokenization_result(result):
    with open("tokenization.txt", "w") as tokenization:
        pattern = "%s\n"
        for word in result:
            tokenization.write(pattern % word)

archive = zipfile.ZipFile('../task_1/archive.zip', 'r')

all_tokens = set()
count = 1
for file in archive.filelist:
    html = archive.open(file.filename)
    text = BeautifulSoup(html, features="html.parser").get_text()
    file_tokens = set(nltk.wordpunct_tokenize(text))
    file_tokens = exclude_stop_words(file_tokens)
    file_tokens = exclude_punctuation(file_tokens)
    file_tokens = exclude_trash(file_tokens)
    file_tokens = exclude_numeric(file_tokens)
    file_tokens = split_camel_case(file_tokens)
    all_tokens = all_tokens.union(file_tokens)
    print("{}/{}".format(count, len(archive.filelist)))
    count += 1

write_tokenization_result(all_tokens)
write_lemmatization_result(lemmatization(all_tokens))
