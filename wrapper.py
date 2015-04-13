"""
Collates other programs into a single wrapper.
"""
from songtext import get_lyrics # get_lyrics(artist, song) -> string
from make_echonest_database import Song_data # class which features a ton of info.
from os.path import exists
import pickle




def add_lyrics_and_song_data_to_database(artist, song):
    """
    what it ways on the tin.
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
    if exists('billboard_song_list.txt'):
        billboard_song_file = open('billboard_song_list.txt', 'r')
        list_of_songs_to_add = pickle.load(billboard_song_file)
    else:
        list_of_songs_to_add = []
    list_of_songs_to_add.extend([('Bob Dylan', 'Like a Rolling Stone'), ('Maroon 5', 'Sugar'), ('Ellie Goulding', 'Love Me Like You Do'), ('Taylor Swift', 'Style'), ('Taylor Swift', 'Blank Space'), ('Hozier', 'Take Me to Church'), ('WALK THE MOON', 'Shut Up And Dance'), ('Ariana Grande', 'One Last Time'), ('Sia', 'Chandelier'), ('Eric Paslay', 'She Don\'t Love You'), ('Red Hot Chili Peppers', 'Under the Bridge'), ('Rihanna', 'Stay'), ('A Great Big World', 'Say Something')]) # a couple baselines b/c woohoo music.
    for entry in list_of_songs_to_add:
        add_lyrics_and_song_data_to_database(entry[0], entry[1])