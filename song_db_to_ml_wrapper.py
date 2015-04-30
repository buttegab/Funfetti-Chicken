"""
Combines the moods, the training data, and the ML code into one program. This program pulls data from the full_database.txt file. Due to irregularities in the
prediction code, sometimes multiple runs are necessary in order to return a reasonable prediction.

"""

import make_echonest_database
import pickle
from sklearn import svm
from sklearn.metrics import confusion_matrix
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

moods_of_interest = ['Yearning', 'Brooding', 'Excited', 'Empowering']

for song in song_data_list:
    if song.mood1 != 'N/A' and song.id != 'N/A' and song.lyrics != '' and song.mood1_text in moods_of_interest and song.parameter_dict['speechiness'] != None:

        usable_songs.append(song)

parameters = [] # train x
moodout = [] # train y
currentSong = [] #Unknown song

mood_to_small_integer = {'Yearning': 0, "Brooding": 1, "Excited": 2, "Empowering": 3}

for i in usable_songs:
    # print i.name
    parameters.append([i.parameter_dict[k] for k in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy','sentiment']])
    moodout.append(mood_to_small_integer[i.mood1_text])

from sklearn.preprocessing import scale

parameters = scale(parameters)

# pprint.pprint(zip(moodout, parameters))

# for i in moodout:
#     if type(i) != int:
#         print i
#         print 'is not an int'

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression


parameters_train, parameters_test, moodout_train, moodout_test  = train_test_split(parameters, moodout, train_size=0.8)

val_counts = [moodout_train.count(0), moodout_train.count(1), moodout_train.count(2), moodout_train.count(3)]
print val_counts

#lin_clf = svm.LinearSVC()
lin_clf = svm.SVC(kernel='linear',C=100000)
#lin_clf = LogisticRegression()
print len(parameters_train), len(parameters_test), len(parameters)
total_weight = sum([1.0/val_counts[v] for v in moodout_train])
print parameters[0]
lin_clf.fit(parameters_train, moodout_train, sample_weight=[1.0/val_counts[v]/total_weight for v in moodout_train])
print lin_clf

# print parameters[173]
# print moodout[173]
predictList = []
accuracy = 0.0
for i in range(len(parameters_test)):
    #print i
    prediction = lin_clf.predict(parameters_test[i])
    predictList.append(prediction)
    #print("Predicted: {}; Actual: {}".format(prediction, moodout[i]))
    accuracy += float(prediction == moodout_test[i])/len(parameters_test)
confusion = confusion_matrix(moodout_test, predictList)
print confusion
import numpy as np
print np.sum(confusion,axis=1)
list2 = np.sum(confusion,axis=1)
for sumn in range(0,4):
    print(float(confusion[sumn][sumn])/float(list2[sumn]))
    #print(confusion[sumn][sumn])
    #print(list2[sumn])

accuracy = accuracy * 100
print accuracy
if accuracy <= 30:
	print("Accuracy too low, please run again")

#print(confusion_matrix(moodout, prediction))

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