"""
Creates a large database for use with the ml code. Collects and formats the artists and song names required for the the other code to gather information
and then for the ml to learn and train on. Scans the last 57 years of data for the top 100 songs for every week off the billboard website. 
"""

import pickle
import make_echonest_database
from get_a_bunch_of_songs import condense_list
import time
from os.path import exists

f = open('all_billboard_songs.txt', 'r+')

tons_of_songs = pickle.load(f)
full_list = tons_of_songs

def add_to_db(artist, song, db):
    """
    Adds song name and artist to database.
    """
    if exists(db):
        f = open(db, 'r+')
        song_list = pickle.load(f)
        curr = make_echonest_database.Song_data(artist, song)
        if curr.id in [prev.id for prev in song_list]:
            if curr.id == "N/A":
                print "Could not find " + song + " : " + artist + "in echonest."
            else:
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

#controls what is added to the database and handles errors and exceptions
for (x, y) in full_list:
    try:
        add_to_db(x, y, 'fifty_seven_years_database.txt')
    except:
        print 'failed: ' + str(x) + ':' + str(y) + '. Retrying.'
        time.sleep(10)
        try:
            add_to_db(x, y, 'fifty_seven_years_database.txt')
        except: 
            print 'failed: ' + str(x) +  ':' + str(y) + '. Skipping.'
    wait_index += 1

    print wait_index

    if wait_index%100 == 0:
        time.sleep(61) # keeping us healthily below the 120 calls per minute requirement. If I were to write this again, I'd add in some sort of time-tracking thing to make it faster / waste less time, but it worked for what it needed to do.