"""
100 страниц в интернете решил не искать, а взять 100 различных страниц с википедии. Википедия, потому что все страницы
ведут на википедию. Если взять, например, какой-нибудь новостной портал, одной из первых ссылок на нем будет ввести на
facebook или youtube, что не очень скажется на контенте страниц, так как все страницы будут в рамках этих двух сайтов.
"""
import zipfile

import httplib2
from bs4 import BeautifulSoup, SoupStrainer

COUNT = 150
http = httplib2.Http()
domen = "https://ru.wikipedia.org"

def full_url(path):
    return domen + path

def handle_page(path, num):
    # Добавляем урл с номареом в виде "1 - https://ru.wikipedia.org/" в файл index.txt
    with open("task_1/index.txt", "a") as index:
        index.write("{} - {}\n".format(str(num), full_url(path)))

    # Добавляем страницу в архив
    status, response = http.request(full_url(path))
    with zipfile.ZipFile('task_1/archive.zip', 'a') as zipped_f:
        zipped_f.writestr("file_{}.html".format(num), response)

paths = ["/wiki/The_Rolling_Stones"]
num = 0



while (len(paths) < COUNT - 1):
    # Переходим по странице num
    # Если статус ОК:
    # 	Добавляем все ссылки в список, которых еще в списке нет
    # 	Обработка страницы
    # 	Увеличиваем num
    # Иначе:
    #   удаляем страницу num со списка
    status, response = http.request(full_url(paths[num]))
    if (status["status"] == "200"):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if len(paths) >= COUNT:
                break
            if link.has_attr('href'):
                path = str(link['href'])
                if (path.startswith("/wiki") and paths.count(path) == 0 and all(s not in path for s in [':', '.'])):
                    paths.append(path)
                    handle_page(path, num)
                    num += 1
    else:
        paths.pop(num)

num += 1

while num <= COUNT and num < len(paths):
    # Если статус ОК:
	# 	обработка страницы
	# 	Увеличиваем num
	# Иначе:
	# 	удаляем страницу num со списка
    path = paths[num]
    status, response = http.request(full_url(path))
    if (status["status"] == "200"):
        handle_page(path, num)
        num += 1
    else:
        paths.pop(num)

print("{} обработаных страниц".format(num - 1))
