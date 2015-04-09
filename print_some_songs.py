import pickle
f = open('billboard_song_list.txt', 'r')

songs = pickle.load(f)
for song in songs:
    print song[0] + " : " + song[1]