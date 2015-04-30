"""
Combines the moods, the training data, and the ML code into one program. This program pulls data from the full_database.txt file. Due to irregularities in the
prediction code, sometimes multiple runs are necessary in order to return a reasonable prediction.

"""

import make_echonest_database
import pickle
from sklearn import svm
import pprint
import requests
from pyechonest import config
config.ECHO_NEST_API_KEY="DCPW87SS20PQ4RXDR"
from pattern.en import *
from swampy.Gui import *


def get_data(artist, title):
    from pyechonest import song
    parameters = []
    #artist = 'coldplay'
    #title = 'clocks'
    rkp_results = song.search(artist=artist,title=title)
    song = rkp_results[0]
    song.audio_summary['sentiment'] = 0
    parameters.append([song.audio_summary[k] for k in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy', 'sentiment']])
    return parameters




f = open('full_database.txt', 'r+')

song_data_list = pickle.load(f)

song_data_list = song_data_list[1:] # gets rid of the first entry, which is kind of broken.

usable_songs = []

moods_of_interest = ['Empowering','Yearning', 'Defiant', 'Sensual', 'Cool', 'Excited', 'Energizing', 'Urgent']

for song in song_data_list:
    if song.mood1 != 'N/A' and song.id != 'N/A' and song.lyrics != '' and song.mood1_text in moods_of_interest and song.parameter_dict['speechiness'] != None:

        usable_songs.append(song)

parameters = [] # train x
moodout = [] # train y
currentSong = [] #Unknown song

mood_to_small_integer = {'Empowering': 0, 'Yearning': 1, "Defiant": 2, "Sensual": 3, "Cool": 4, "Excited": 5, "Energizing": 6, "Urgent": 7, "Rowdy": 8, "Brooding": 9}

for i in usable_songs:
    # print i.name
    parameters.append([i.parameter_dict[k] for k in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy','sentiment']])
    moodout.append(mood_to_small_integer[i.mood1_text])

# pprint.pprint(zip(moodout, parameters))

# for i in moodout:
#     if type(i) != int:
#         print i
#         print 'is not an int'

lin_clf = svm.LinearSVC()
lin_clf.fit(parameters, moodout)

accuracy = 0.0
# print parameters[173]
# print moodout[173]

for i in range(len(parameters)):
    #print i
    prediction = lin_clf.predict(parameters[i])
    #print("Predicted: {}; Actual: {}".format(prediction, moodout[i]))
    accuracy += float(prediction == moodout[i])/len(parameters)

accuracy = accuracy * 100
if accuracy <= 30:
	print("Accuracy too low, please run again")

def get_mood(artist,track):
    songdata = get_data(artist,track)
    prediction = lin_clf.predict(songdata)
    if accuracy>= 30:
        #print("Mood: {}".format(prediction))
        return prediction[0]

foods = {0:'Banana', 1:'Bananas', 2:'Plantain', 3:'Plantains', 4:'Apple Bananas', 5:'Apple Banana', 6:'Florida', 7:'Banana Cream Pie', 8:'Banana Cream Pies', 9:'New Hampshire'}


def show_food(artist,track):
    mood = get_mood(artist,track)
    text = g.te(width=25, height=1)
    text.insert(END,foods[mood])

g = Gui()
g.title('Funfetti Chicken')
label = g.la(text='Enter a song and artist below')
artist = g.en(text = 'Rick Astley')
track = g.en(text = 'Never Gonna Give You Up')
button = g.bu(text="Feed Me", command=lambda : show_food(artist.get(),track.get()))
g.mainloop()

# get_mood('coldplay','clocks')