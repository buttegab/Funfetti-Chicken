"""
whatevs :P.

"""

import make_echonest_database
import pickle
from sklearn import svm
import pprint

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

mood_to_small_integer = {'Empowering': 0, 'Yearning': 1, "Defiant": 2, "Sensual": 3, "Cool": 4, "Excited": 5, "Energizing": 6, "Urgent": 7, "Rowdy": 8, "Brooding": 9}

for i in usable_songs:
    # print i.name
    parameters.append([i.parameter_dict[k] for k in ['tempo', 'mode', 'key', 'sentiment', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy']])
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
    print i
    prediction = lin_clf.predict(parameters[i])
    print("Predicted: {}; Actual: {}".format(prediction, moodout[i]))
    accuracy += float(prediction == moodout[i])/len(parameters)

accuracy = accuracy * 100
print("Accuracy: {}%".format(accuracy))