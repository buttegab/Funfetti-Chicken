"""
Gets a frikkin' *ton* of songs from Billboard. NOTE THAT THIS TAKES A WHILE TO RUN. This isn't due to code slowness, it's because the Billboard server gets mad if you try to request too many things too quickly--so, I introduced a few 90-second weights during the runtime to let it chill out.
-Matt
"""

import requests
import time
import random
import pickle
from os.path import exists
from bs4 import BeautifulSoup


def get_three_years_of_billboard_songs():
    """
    what it says on the tin. Goes through three years worth of songs, beginning April 7th 2012, and gets *all* of the "Billboard Top 100" songs from that week -- from the Billboard website. Returns this as a giant list.
    -Matt
    """
    month_to_length_dictionary = {1: 31, 2: 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    year = 2004
    month = 03
    day = 27

    artist_and_song_list = []

    for i in range(200):

        # "creates" a new URL to parse.
        url = 'http://www.billboard.com/charts/hot-100/%04d-%02d-%02d' % (year, month, day)
        print url # Feel free to comment this out. It's just a "progress bar" of sorts, and helps diagnose if something goes wrong.

        # Uses requests and BeautifulSoup to get artists & songs from that URL, and adds it to the list of artists and songs.

        r = requests.get(url)
        while r.status_code != 200:
            time.sleep(60)
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

        day += 7 # Adjusts the day, date, and URL by a week so that the next loop gets the next week's songs.
        if day > month_to_length_dictionary[month]:
            day = day%month_to_length_dictionary[month]
            month += 1
        if month > 12:
            month = 1
            year += 1

        # waits a little while, because otherwise the billboard server identifies it as an attack, virus, or glitch (and stops answering):

        time.sleep(random.choice([i for i in range(20, 40)]))

    return artist_and_song_list

def get_all_the_billboard_songs():
    """
    fifty-seven years worth, give or take.
    http://www.billboard.com/charts/hot-100/1958-11-29
    """
    month_to_length_dictionary = {1: 31, 2: 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    year = 1958
    month = 11
    day = 29

    artist_and_song_list = []
    i = 0

    while year < 2015 or month < 4:
        i += 1 # keeps track of partial completions.
        # "creates" a new URL to parse.
        url = 'http://www.billboard.com/charts/hot-100/%04d-%02d-%02d' % (year, month, day)
        print url # Feel free to comment this out. It's just a "progress bar" of sorts, and helps diagnose if something goes wrong.

        # Uses requests and BeautifulSoup to get artists & songs from that URL, and adds it to the list of artists and songs.

        try:
            r = requests.get(url)
            # while r.status_code != 200:
            #     time.sleep(60)
            #     r = requests.get(url)
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
        except:
            print "error at" + str(year) + '-' + str(month) + '-' + str(day)
            time.sleep(60)
            pass
        # updates the day/date to get the next week's Billboard URL.
        day += 7 # Adjusts the day, date, and URL by a week so that the next loop gets the next week's songs.
        if day > month_to_length_dictionary[month]:
            day = day%month_to_length_dictionary[month]
            month += 1
        if month > 12:
            month = 1
            year += 1
            if year%4 == 0:
                month_to_length_dictionary[2] = 29
            else:
                month_to_length_dictionary[2] = 28
        if i%400 == 0:
            print i
            if exists('temporary_file.txt'):
                temp_file = open('temporary_file.txt', 'r+')
            else:
                temp_file = open('temporary_file.txt', 'w')
            temp_file.seek(0,0)
            pickle.dump(artist_and_song_list, temp_file)

        # waits a little while, because otherwise the billboard server identifies it as an attack, virus, or glitch (and stops answering):

        time.sleep(random.randint(2,8))
    return artist_and_song_list



def condense_list(input_list):
    """
    Simplifies a list to only list songs/artists one time. In other words, ['A','A','A','B','C','C','D'] gets turned into ['A','B','C','D']. -M
    """
    condensed_list = []

    for entry in input_list:
        if entry not in condensed_list:
            condensed_list.append(entry)

    return condensed_list


if __name__ == "__main__":
    """
        If the function already ran successfully, then it just says 'list already found.' Otherwise, it runs the get-three-years-of-songs function, condenses the list, and pickles it. -M
    """
    if exists('yet_more_billboard_songs.txt'):
        print "list already found"
    else:
        huge_song_list = get_all_the_billboard_songs()
        less_huge_song_list = condense_list(huge_song_list)
        f = open('yet_more_billboard_songs.txt', 'w')
        f.seek(0,0)
        pickle.dump(less_huge_song_list, f)