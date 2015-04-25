"""
Helps print stuff out.
"""

import make_echonest_database
import pickle


f = open('full_database.txt', 'r+')

song_data_list = pickle.load(f)

song_data_list = song_data_list[1:] # gets rid of the first entry, which is kind of broken.

usable_songs = []

moods_of_interest = ['Empowering','Yearning', 'Defiant', 'Sensual', 'Cool', 'Excited', 'Energizing', 'Urgent', 'Rowdy', 'Brooding']

for song in song_data_list:
    if song.mood1 != 'N/A' and song.id != 'N/A' and song.lyrics != '' and song.mood1_text in moods_of_interest:
        usable_songs.append(song)

mood_count = {}

for song in usable_songs:
    if song.mood1 in mood_count:
        mood_count[song.mood1] += 1
    else:
        mood_count[song.mood1] = 1
    # if song.mood2_text in mood_count:
        # mood_count[song.mood2_text] += 1
    # else:
        # mood_count[song.mood2_text] = 1

moods_in_order = sorted(mood_count, key=mood_count.get, reverse=True)

number_of_moods = 0

for a in moods_in_order:
    print str(mood_count[a]) + '\t' + a
    number_of_moods += mood_count[a]

# print len(usable_songs)
# print len(usable_songs) * 2
print number_of_moods

# print len(song_data_list)
print len(usable_songs)

"""

427 Empowering 42945
200 Yearning 65325
172 Defiant 42951
153 Sensual 42947
147 Cool 65326
120 Excited 42960
117 Energizing 42961
113 Urgent 42955
67  Rowdy 65330
61  Brooding 65329
44  Upbeat
33  Sophisticated
27  Romantic
24  Aggressive
17  Sentimental
14  Gritty
14  Melancholy
12  Fiery
6   Easygoing
5   Lively
4   Stirring
1   Tender

"""