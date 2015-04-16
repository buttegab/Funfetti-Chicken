import requests
from bs4 import BeautifulSoup

month_to_length_dictionary = {1: 31, 2: 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

# for i in range(1,13):
#     print month_to_length_dictionary[i]


# initial_url = 'http://www.billboard.com/charts/hot-100/2012-04-07'

year = 2012
month = 04
day = 07

for i in range(157):
    url = 'http://www.billboard.com/charts/hot-100/%04d-%02d-%02d' % (year, month, day)
    # print url
    day += 7
    if day > month_to_length_dictionary[month]:
        day = day%month_to_length_dictionary[month]
        month += 1
    if month > 12:
        month = 1
        year += 1

# print "testing leading zeros: %02d" % (7)

import requests
# import bs4
from bs4 import BeautifulSoup

url = 'http://www.billboard.com/charts/hot-100/2015-02-21'
r = requests.get(url)
# print r.encoding
# r.encoding = 'utf-8'
# print r.encoding
# print r.text
# print r.text.encode('ascii', 'ignore')
html_file = r.text.encode('ascii', 'ignore')
test_page = BeautifulSoup(html_file)
artist_and_song_list = []
# print test_page.title.string
for entry in test_page.find_all('article', {"class": "chart-row"}):
    name = entry.find('div', 'row-title').contents[1].string.strip()
    if (entry.find('div', 'row-title').contents[3].find('a') != -1):
        artist = entry.find('div', 'row-title').contents[3].a.string.strip()
    else:
        artist = entry.find('div', 'row-title').contents[3].string.strip()
    # print name + ': ' + artist
    artist_and_song_list.append((str(artist), str(name)))
# print test_page.find_all('a')

print artist_and_song_list


if __name__ == "__main__":
    pass