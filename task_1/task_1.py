"""
100 страниц в интернете решил не искать, а взять 100 различных страниц с википедии. Википедия, потому что все страницы
ведут на википедию. Если взять, например, какой-нибудь новостной портал, одной из первых ссылок на нем будет ввести на
facebook или youtube, что не очень скажется на контенте страниц, так как все страницы будут в рамках этих двух сайтов.
"""
import zipfile

import httplib2
from bs4 import BeautifulSoup, SoupStrainer

COUNT = 100
http = httplib2.Http()


def handle_page(url, num):
    # Добавляем урл с номареом в виде "1 - https://ru.wikipedia.org/" в файл index.txt
    with open("index.txt", "a") as index:
        index.write("{} - {}\n".format(str(num), url))

    # Добавляем страницу в архив
    status, response = http.request(url)
    with zipfile.ZipFile('archive.zip', 'a') as zipped_f:
        zipped_f.writestr("file_{}.html".format(num), response)


urls = ["https://ru.wikipedia.org/"]
num = 0



while (len(urls) < COUNT - 1):
    # Переходим по странице num
    # Если статус ОК:
    # 	Добавляем все ссылки в список, которых еще в списке нет
    # 	Обработка страницы
    # 	Увеличиваем num
    # Иначе:
    #   удаляем страницу num со списка
    status, response = http.request(urls[num])
    if (status["status"] == "200"):
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                url = str(link['href'])
                if (url.startswith("http") and urls.count(url) == 0):
                    urls.append(url)
                    handle_page(url, num)
                    num += 1
    else:
        urls.pop(num)

num += 1

while num <= COUNT and num < len(urls):
    # Если статус ОК:
	# 	обработка страницы
	# 	Увеличиваем num
	# Иначе:
	# 	удаляем страницу num со списка
    url = urls[num]
    status, response = http.request(url)
    if (status["status"] == "200"):
        handle_page(url, num)
        num += 1
    else:
        urls.pop(num)

print("{} обработаных страниц".format(num))
