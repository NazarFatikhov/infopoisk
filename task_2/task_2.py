import zipfile
import nltk
import pymorphy2

from bs4 import BeautifulSoup
from filters import filter_tokens

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
    file_tokens = filter_tokens(file_tokens)
    all_tokens = all_tokens.union(file_tokens)
    print("{}/{}".format(count, len(archive.filelist)))
    count += 1

write_tokenization_result(all_tokens)
write_lemmatization_result(lemmatization(all_tokens))
