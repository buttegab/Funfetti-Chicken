"""
Collates other programs into a single wrapper.
"""
from songtext import get_lyrics # get_lyrics(artist, song) -> string
from make_echonest_database import Song_data # class which features a ton of info.
from os.path import exists
import pickle
import time




def add_lyrics_and_song_data_to_database(artist, song):
    """
    what it ways on the tin. Adds the artist + song to the database, using the Song_data class from make_echonest_database.py
    Then, stores this new object of artist+song in song_database.txt
    -Matt
    """
    if exists('song_database.txt'):
        f = open('song_database.txt', 'r+')
        song_list = pickle.load(f)
        current_entry = Song_data(artist, song)
        if current_entry.id in [previous_entry.id for previous_entry in song_list]:
            print "Song '" + song + "' already in database."
            return
        song_list.append(current_entry)
        f.seek(0,0)
        pickle.dump(song_list, f)
    else:
        f = open('song_database.txt', 'w')
        song_list = [Song_data(artist, song)]
        f.seek(0,0)
        pickle.dump(song_list, f)


if __name__ == "__main__":
    """
    When run as main, it loads the songs from billboard_song_list.txt, which were generated by the get_a_bunch_of_songs.py script. It then adds every song in that list to the song_database.txt database file.
    Every. Flipping. Song.

    Since the API can only call so many times per minute, this program waits for 120 seconds every few dozen calls. As such, it takes ten-twenty-ish minutes to run, with a good internet connection + computer.
    -Matt
    """
    if exists('billboard_song_list.txt'):
        billboard_song_file = open('billboard_song_list.txt', 'r')
        list_of_songs_to_add = pickle.load(billboard_song_file) # gets a giant list of popular songs. This list was pre-generated by another script.
    else:
        list_of_songs_to_add = []
    list_of_songs_to_add.extend([('Bob Dylan', 'Like a Rolling Stone'), ('Maroon 5', 'Sugar'), ('Ellie Goulding', 'Love Me Like You Do'), ('Taylor Swift', 'Style'), ('Taylor Swift', 'Blank Space'), ('Hozier', 'Take Me to Church'), ('WALK THE MOON', 'Shut Up And Dance'), ('Ariana Grande', 'One Last Time'), ('Sia', 'Chandelier'), ('Eric Paslay', 'She Don\'t Love You'), ('Red Hot Chili Peppers', 'Under the Bridge'), ('Rihanna', 'Stay'), ('A Great Big World', 'Say Something')]) # a couple baselines b/c woohoo music.
    waiting_index = 0
    for (x, y) in list_of_songs_to_add:
        add_lyrics_and_song_data_to_database(x, y)
        waiting_index += 1
        print waiting_index # so that in the event of connection loss or unknown error in the middle, you don't need to redo the entire thing.
        if waiting_index%40 == 0:
            time.sleep(120) # conforming to api rate limits