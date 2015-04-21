"""
"Cleans up" the database pickle file thing: gives all objects in the database a boolean [object].complete, based on whether we have an ID, lyrics, and a mood. Currently doesn't actually take in mood, but that's trivial to add.
Currently, this code doesn't do anything useful. It will once the Song_data.mood stuff works.
-Matt
"""

import pickle

f = open('song_database.txt', 'r+')
database = pickle.load(f)

for entry in database:
    if entry.lyrics == '' or entry.id == "SONG NOT FOUND" or entry.mood == None: # if [no lyrics were found] or [echonest didn't find the song] or [the mood database didn't have the song], this flags the object as not useful for ML purposes.
        entry.usable = False
    else:
        entry.usable = True

f.seek(0,0)
pickle.dump()