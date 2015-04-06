import requests
# import bs4
from bs4 import BeautifulSoup

url = 'http://www.billboard.com/charts/hot-100/2015-02-21'
r = requests.get(url)
print r.encoding
# r.encoding = 'utf-8'
# print r.encoding
# print r.text
# print r.text.encode('ascii', 'ignore')
html_file = r.text.encode('ascii', 'ignore')
test_page = BeautifulSoup(html_file)
print test_page.title.string
for entry in test_page.find_all('article', {"class": "chart-row"}):
    name = entry.find('div', 'row-title').contents[1].string.strip()
    if (entry.find('div', 'row-title').contents[3].find('a')):
        artist = entry.find('div', 'row-title').contents[3].a.string.strip()
    else:
        artist = entry.find('div', 'row-title').contents[3].string.strip()
    print name + ': ' + artist
# print test_page.find_all('a')


if __name__ == "__main__":
    pass