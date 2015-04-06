"""
Gets a frikkin' *ton* of songs from Billboard. NOTE THAT THIS TAKES A WHILE TO RUN. This isn't due to code slowness, it's because the Billboard server gets mad if you try to request too many things too quickly--so, I introduced a few 90-second weights during the runtime to let it chill out.
-Matt
"""

import requests
import time
import random
from bs4 import BeautifulSoup


def get_three_years_of_billboard_songs():
    """
    what it says on the tin.
    """
    month_to_length_dictionary = {1: 31, 2: 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    year = 2012
    month = 04
    day = 07

    artist_and_song_list = []

    for i in range(157):

        # "creates" a new URL to parse.
        url = 'http://www.billboard.com/charts/hot-100/%04d-%02d-%02d' % (year, month, day)
        print url # Feel free to comment this. It's just a "progress bar" of sorts, and helps diagnose if something goes wrong.

        # Uses requests and BeautifulSoup to get artists & songs from that URL, and adds it to the list of artists and songs.

        r = requests.get(url)
        html_file = r.text.encode('ascii', 'ignore')
        page = BeautifulSoup(html_file)

        for entry in page.find_all('article', {'class': 'chart-row'}):
            contents = entry.find('div', 'row-title').contents
            name = contents[1].string.strip()
            if contents[3].find('a'):
                artist = contents[3].a.string.strip()
            else:
                artist = contents[3].string.strip()
            artist_and_song_list.append((str(artist), str(name)))

        # updates the day/date to get the next week's Billboard URL.

        day += 7
        if day > month_to_length_dictionary[month]:
            day = day%month_to_length_dictionary[month]
            month += 1
        if month > 12:
            month = 1
            year += 1

        # waits a little while, because otherwise the billboard server identifies it as an attack, virus, or glitch (and stops answering):
        time.sleep(random.choice([i + j for j in range(10)]))

    condensed_list = []

    for entry in artist_and_song_list:
        if entry not in condensed_list:
            condensed_list.append(entry)

    return condensed_list

if __name__ == "__main__":
    print get_three_years_of_billboard_songs()