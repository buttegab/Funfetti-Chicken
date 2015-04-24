"""
shelf explanatory
"""

import pickle
import make_echonest_database
from get_a_bunch_of_songs import condense_list
import time
from os.path import exists

f = open('billboard_song_list.txt', 'r+')
g = open('more_billboard_songs.txt', 'r+')

recent_songs = pickle.load(f)
less_recent_songs = pickle.load(g)
recent_songs.extend(less_recent_songs)

full_list = condense_list(recent_songs)


def add_to_db(artist, song, db):
    """
    what it says on the tin.
    """
    if exists(db):
        f = open(db, 'r+')
        song_list = pickle.load(f)
        curr = make_echonest_database.Song_data(artist, song)
        if curr.id in [prev.id for prev in song_list]:
            print "Song '" + song + "' already in database."
            return
        song_list.append(curr)
        f.seek(0,0)
        pickle.dump(song_list, f)
    else:
        f = open(db, 'w')
        song_list = [make_echonest_database.Song_data(artist, song)]
        f.seek(0,0)
        pickle.dump(song_list, f)


wait_index = 0 # to keep track of api rate limits.


for (x, y) in full_list:
    try:
        add_to_db(x, y, 'full_database.txt')
    except:
        time.sleep(60)
        try:
            add_to_db(x, y, 'full_database.txt')
        except:
            pass
    wait_index += 1

    print wait_index

    if wait_index%40 == 0:
        time.sleep(70)