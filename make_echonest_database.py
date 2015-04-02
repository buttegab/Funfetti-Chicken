"""
Makes a database of songs, and their associated values, through using the Echo Nest API. Organized as a list of objects:

[ [song 1 list], [song 2 list], ...];
song 1 list = [name, artist, tempo, mode, key, danceability, acousticness, speechiness].

Saved via the Pickle module.

-Matt

"""

import pyechonest
from pyechonest import config, song
import pickle
import string
from os.path import exists

config.ECHO_NEST_API_KEY = "NOLYZICKJ6J3JQ7LS"

class Song_data:
    def __init__(self, artist, name):
        self.artist = artist
        self.name = name
        current_song = song.search(artist = artist, title = name)[0]
        self.id = current_song.id
        # self.id = current_song.id
        self.parameter_dict = {x: current_song.audio_summary[x] for x in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy']}

    def __str__(self):
        return self.name + " - " + self.artist

def print_test_info():
    like_a_rolling_stone = Song_data('Bob Dylan', 'Like a Rolling Stone')
    print(like_a_rolling_stone)
    print like_a_rolling_stone.parameter_dict['tempo']

def add_song_to_database(artist, name):
    """
    TODO: Make it not duplicate songs, in a more efficient manner.
    """
    if exists('pickled_songs.txt'):
        f = open('pickled_songs.txt', 'r+')
        song_list = pickle.load(f)
        current_entry = Song_data(artist, name);
        if current_entry.id in [previous_entry.id for previous_entry in song_list]:
            print "Song '" + name + "' already in database."
            return
        song_list.append(current_entry)
        f.seek(0,0)
        pickle.dump(song_list, f)
    else:
        f = open('pickled_songs.txt', 'w')
        song_list = [Song_data(artist, name)]
        f.seek(0,0)
        pickle.dump(song_list, f)

if __name__ == "__main__":
    # for (x,y) in [('Bob Dylan', 'Like a Rolling Stone'), ('Maroon 5', 'Sugar'), ('Ellie Goulding', 'Love Me Like You Do'), ('Taylor Swift', 'Style'), ('Taylor Swift', 'Blank Space'), ('Hozier', 'Take Me to Church'), ('WALK THE MOON', 'Shut Up And Dance'), ('Ariana Grande', 'One Last Time'), ('Sia', 'Chandelier'), ('Eric Paslay', 'She Don\'t Love You'), ('Red Hot Chili Peppers', 'Under the Bridge'), ('Rihanna', 'Stay'), ('A Great Big World', 'Say Something')]:
        # add_song_to_database(x, y)
        pass
    # print_test_info();
    # if exists('pickled_songs.txt'):
    #     f = open('pickled_songs.txt', 'r+')
    #     song_list = pickle.load(f)
    # else:
    #     song_list = [Song_data(x,y) for (x,y) in [('Bob Dylan', 'Like a Rolling Stone'), ('Maroon 5', 'Sugar'), ('Ellie Goulding', 'Love Me Like You Do'), ('Taylor Swift', 'Style'), ('Taylor Swift', 'Blank Space'), ('Hozier', 'Take Me to Church'), ('WALK THE MOON', 'Shut Up And Dance'), ('Ariana Grande', 'One Last Time'), ('Sia', 'Chandelier'), ('Eric Paslay', 'She Don\'t Love You'), ('Red Hot Chili Peppers', 'Under the Bridge'), ('Rihanna', 'Stay'), ('A Great Big World', 'Say Something')]]
    #     pickle.dump(song_list, open('pickled_songs.txt', 'w'))

