"""
Regression analysis infrastrucure. 
Independent variables: tempo, key, whatever the pattern stuff is.
Dependent variables, aka output / training, = moods. Possibly multiple; right now, just 1. Continuous.
-Matt
"""




"""
Ideally, we will have code that goes like this:

input_data = [(song.tempo, song.lyric_sentiment, song.key) for song in song_database]
output_data =[(song.happiness, song.excitedness) for song in song_database]

scikit_learn(input_data, output_data)
"""


from sklearn.svm import SVR
import numpy
import pickle

f = open(cleaned_song_database.txt, 'r')

song_object_list = pickle.load(f)

input_data = [(song.parameter_dict[tempo], song.parameter_dict[key], song.lyric_sentiment) for song in song_object_list]

output_data = [(song.happiness, song.etc) for song in song_object_list]

number_of_samples = len(song_object_list)

fitting_function = SVR(C=1.0, epsilon=0.1)
fitting_function.fit(input_data[:int(number_of_samples/2)], output_data[:int(number_of_samples/2)])



"""
NOTE: SVR might not be computationally efficient. The sklearn implementation might only accept 1 output variable at a time; as such, might need to be run independently for each of the emotion parameters.
"""

#testing it:
test_results = []
for i in range(int(number_of_samples/2),number_of_samples):
    test_results.append(fitting_function.predict(input_data[i]) - output_data[i]) # generates a list of the "errors" from the function.
# fitting_function.predict()