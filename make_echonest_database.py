"""
Makes a database of songs, and their associated values, through using the Echo Nest API. Organized as a list of objects:

[ [song 1 list], [song 2 list], ...];
song 1 list = [name, artist, tempo, mode, key, danceability, acousticness, speechiness].

Saved via the Pickle module.


"""

import pyechonest
from pyechonest import config, song
import pickle
# import string
from os.path import exists
import pygn
from pattern.en import sentiment
import requests
# import math


config.ECHO_NEST_API_KEY = "NOLYZICKJ6J3JQ7LS"


class Song_data:

    def __init__(self, artist, name):
        self.artist = artist
        self.name = name
        temp = song.search(artist = artist, title = name) # Puts pyechonest info from searching for the song into a temporary variable.
        if len(temp) != 0: #checks whether there were results. If there were, it takes the first result and stores the key + tempo + mode + etc. data for it.
            current_song = temp[0]
            self.id = current_song.id
            self.lyrics = self.get_lyrics()
            self.parameter_dict = {}
            self.mood_dict = self.get_mood()
            if len(self.mood_dict) >= 2:
                self.mood1 = self.mood_dict['1']['ID']
                self.mood1_text = self.mood_dict['1']['TEXT']
                self.mood2 = self.mood_dict['2']['ID']
                self.mood2_text = self.mood_dict['2']['TEXT']
            else:
                self.mood1 = 'N/A'
            # self.paramete_dict['mood1'] = self.mood_dict['1']['ID']
            self.parameter_dict['sentiment'] = sentiment(self.lyrics)[0]
            for x in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy']:
                self.parameter_dict[x] = current_song.audio_summary[x]
        else:
            self.id = 'N/A' #If there weren't results, it sets the ID as 'N/A'.


    def __str__(self):
        return self.name + " - " + self.artist


    def get_mood(self):
        """
            Returns the mood data for the self object.
        """
        data = pygn.search(clientID='10189056-547D2643844BF1E2B9E85BD85773AEFE', userID='27678235334765580-1FB57EBF64483B1937D128ACEB314A68', artist=self.artist, track=self.name)
        return data['mood']


    def get_lyrics(self):
        """
            Returns the lyrics for the self object, if the lyricsnmusic API can find it. Else, returns an empty string.
        """
        url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]=' + self.artist + '%20' + self.name
        r = requests.get(url)
        r_text = r.text
        for (old, new) in [('false', 'False'), ('true', 'True'), ('null', 'None')]:
            r_text = r_text.replace(old, new)
        r_text_as_data = eval(r_text)
        if len(r_text_as_data) != 0:
            r_text_dict = r_text_as_data[0]
            return r_text_dict['snippet']
        else:
            return ''


def add_song_to_database(artist, name, db):
    """
        This function loads and/or creates a 'db' file, with pickle. This file stores a list of Song_data objects.
        The function then generates the artist, name Song_data object. If song isn't already in the database, it adds it to the database, and then pickles/packages it back up.
    """
    if exists(db):
        f = open(db, 'r+')
        song_list = pickle.load(f)
        current_entry = Song_data(artist, name);
        if current_entry.id in [previous_entry.id for previous_entry in song_list]:
            print str(current_entry) + " already in database."
            return
        song_list.append(current_entry)
        f.seek(0,0)
        pickle.dump(song_list, f)
    else:
        f = open(db, 'w')
        song_list = [Song_data(artist, name)]
        f.seek(0,0)
        pickle.dump(song_list, f)

if __name__ == "__main__":
    for (x,y) in [('Bob Dylan', 'Like a Rolling Stone'), ('Maroon 5', 'Sugar'), ('Ellie Goulding', 'Love Me Like You Do'), ('Taylor Swift', 'Style'), ('Taylor Swift', 'Blank Space'), ('Hozier', 'Take Me to Church'), ('WALK THE MOON', 'Shut Up And Dance'), ('Ariana Grande', 'One Last Time'), ('Sia', 'Chandelier'), ('Eric Paslay', 'She Don\'t Love You'), ('Red Hot Chili Peppers', 'Under the Bridge'), ('Rihanna', 'Stay'), ('A Great Big World', 'Say Something')]:
        # print x + ' ' + y 
        add_song_to_database(x, y, 'ps.txt') # This tests out the pickling/generation by making a pickle file with data for the above songs.