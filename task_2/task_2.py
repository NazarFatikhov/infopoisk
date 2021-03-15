import zipfile

from bs4 import BeautifulSoup

archive = zipfile.ZipFile('../task_1/archive.zip', 'r')
for file in archive.filelist:
    html = archive.open(file.filename)
    print(BeautifulSoup(html, features="html.parser").get_text())