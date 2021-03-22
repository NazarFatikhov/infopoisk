import zipfile
import nltk

from bs4 import BeautifulSoup
from utils import to_normal_form
from filters import filter_tokens

def read_lemmas():
    lemmas = dict()
    with open("../task_2/lemmatization.txt", "r") as file:
        for row in file:
            row_list = row.split(" ")
            lemmas[row_list[0]] = row_list[1:-1]
        return lemmas

lammas = read_lemmas()
words_in_files = dict()
words_at_all = dict()

archive = zipfile.ZipFile('../task_1/archive.zip', 'r')
i = 1
for file in archive.filelist:
    html = archive.open(file.filename)
    text = BeautifulSoup(html, features="html.parser").get_text()
    words = list(nltk.wordpunct_tokenize(text))
    j = 0
    for w in words:
        word = to_normal_form(w)
        if len(filter_tokens({word})) == 0:
            continue
        if word in words_at_all.keys():
            words_at_all[word] += 1
        else:
            words_at_all[word] = 1
        if word in words_in_files.keys():
            if file.filename in words_in_files[word].keys():
                words_in_files[word][file.filename] += 1
            else:
                words_in_files[word][file.filename] = 1
        else:
            words_in_files[word] = dict()
            words_in_files[word][file.filename] = 1
        # if (j % 100 == 0):
        #     print("{} / {} words in file {}".format(j, len(words), file.filename))
        j += 1
    print("{} / {} - files".format(i, len(archive.filelist)))
    i += 1

print("sort")
words_at_all = dict(sorted(words_at_all.items(), key=lambda item: item[1], reverse=True))

with open("words_at_all.txt", "w") as w_a_l_file, open("words_in_files.txt", "w") as w_i_f_file:
    p = 0.1
    count = 1
    for word in words_at_all:
        files_count = [word]
        for file in words_in_files[word]:
            files_count.append("{}:{}".format(file, words_in_files[word][file]))
        w_i_f_file.write(",".join([str(i) for i in files_count]) + "\n")
        w_a_l_file.write("{}:{}\n".format(word, str(words_at_all[word])))
        if (count > len(words_in_files.keys()) * p):
            print("{}% слов".format(p * 100))
            p += 0.1
        count += 1
