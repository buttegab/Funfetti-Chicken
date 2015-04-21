"""
This is a scaffolding file, used to check whether billboard_song_list.txt contains a pickled list of songs. If it does, then the file prints out those songs (loooots of them).
-Matt
"""

import pickle
f = open('billboard_song_list.txt', 'r')

songs = pickle.load(f)
for song in songs:
    print song[0] + " : " + song[1]