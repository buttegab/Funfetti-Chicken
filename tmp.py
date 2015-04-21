import pickle
import pprint
from make_echonest_database import Song_data
from sklearn import svm

"""
classification:
0 - happy
1 - sad
2 - excited
3 - angry
"""

f = open('pickled_songs.txt', 'r')
song_list = pickle.load(f)
f.close()

# fabricate data
train_x = [list(s.parameter_dict.values()) for s in song_list]
train_y = [0, 0, 0, 1, 2, 1, 2, 1, 3, 1, 1, 1, 1]
# pprint.pprint(zip(train_y, train_x))

# make and train model
lin_clf = svm.LinearSVC()
lin_clf.fit(train_x, train_y)

# test the accuracy
accuracy = 0.0
for i in range(len(train_x)):
	prediction = lin_clf.predict(train_x[i])[0]
	print("Predicted: {0}; Actual: {1}".format(prediction, train_y[i]))
	accuracy += float(prediction == train_y[i])/len(train_x)
accuracy *= 100
print("Accuracy: {0}%".format(accuracy))
