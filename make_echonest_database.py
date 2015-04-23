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
import json
import urllib2
import pygn
from pattern.en import *
import requests
import urllib
import json
import math

config.ECHO_NEST_API_KEY = "NOLYZICKJ6J3JQ7LS"

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def get_lyrics(artist, song):
    """
    Gets lyrics for the given song, if it can be found in the lyricsnmusic api.
    -Matt
    """
    url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]=' + artist+ '%20'+ song
    r = requests.get(url)
    r_text = r.text
    r_text = r_text.replace('false', 'False')
    r_text = r_text.replace('true', 'True')
    r_text = r_text.replace('null', 'None') # converting to something Python understands. These lines just replace 'true' with 'True', 'null' with 'None', etc--since java/c++/html/whatever language the api uses has *slightly* different syntax from python :P.
    r_text_as_data_structure = eval(r_text)
    if len(r_text_as_data_structure) != 0:
        r_text_dictionary = r_text_as_data_structure[0]
        return r_text_dictionary['snippet'] #returns a verse's worth of lyrics, which is all we can automatically get b/c copyright law in the APIs.
    else:
        return '' #means that nothing was found; as such, this is an empty string. This is to prevent a fatal error in the event that for some reason no song is found.

class Song_data:
    def __init__(self, artist, name):
        self.artist = artist
        self.name = name
        temp = song.search(artist = artist, title = name) # This searches echonest's song database for the artist and title, and returns the pyechonest information for it.
        if len(temp) != 0: #checks whether there were results. If there were, it takes the first result and stores the key + tempo + mode + etc. data for it.
            current_song = temp[0]
            self.id = current_song.id
            self.parameter_dict = {'mood': get_mood(self.artist, self.name)},{'sentiment': sentiment(get_lyrics(artist, name))},{x: current_song.audio_summary[x] for x in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy']}
        else:
            self.id = 'SONG NOT FOUND' #If there weren't results, it sets the ID as 'SONG NOT FOUND'.

    def __str__(self):
        return self.name + " - " + self.artist # Makes the object print out as "Name - Artist" rather than <object Song_data @ some_place_with_some_numbers.1234512451512>

def get_mood(artist, name): # Note: I'm not sure what this function is doing. Well, more specifically - this function will return a bunch of information, but in a big list-dictionary-thing. Do we have something to convert this "data" into relevant 'mood' info like "happiness", "sadness", "excitedness", etc? -Matt
    artist = str(artist)
    title = str(name) # Should 'name' be a string here?.. :/ -Matt
    data = pygn.search(clientID='10189056-547D2643844BF1E2B9E85BD85773AEFE', userID='27678235334765580-1FB57EBF64483B1937D128ACEB314A68', artist=artist, track=title)
    return data['mood']

def print_test_info():
    """
        Tests to see whether the basic calls for the Song_data class are working. If Song_data initialization works correctly, then this should print out known info for a song which we're positive exists--in this case, Bob Dylan's 'Like a Rolling Stone'
    """
    like_a_rolling_stone = Song_data('Bob Dylan', 'Like a Rolling Stone')
    print(like_a_rolling_stone)
    print like_a_rolling_stone.parameter_dict['tempo']

def add_song_to_database(artist, name):
    """
        This function loads and/or creates a pickled_songs.txt file, with pickle. This file stores a list of Song_data objects.
        The function then generates the artist, name Song_data object. If song isn't already in the database, it adds it to the database, and then pickles/packages it back up.
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

# if __name__ == "__main__":
#     for (x,y) in [('Bob Dylan', 'Like a Rolling Stone'), ('Maroon 5', 'Sugar'), ('Ellie Goulding', 'Love Me Like You Do'), ('Taylor Swift', 'Style'), ('Taylor Swift', 'Blank Space'), ('Hozier', 'Take Me to Church'), ('WALK THE MOON', 'Shut Up And Dance'), ('Ariana Grande', 'One Last Time'), ('Sia', 'Chandelier'), ('Eric Paslay', 'She Don\'t Love You'), ('Red Hot Chili Peppers', 'Under the Bridge'), ('Rihanna', 'Stay'), ('A Great Big World', 'Say Something')]:
#         add_song_to_database(x, y) # This tests out the pickling/generation by making a pickle file with data for the above songs.

#if __name__ == "__main__": # testing the mood-getting api to figure out how that works.
    #gm_response = get_mood("yellow")
