"""
Combines the moods, an "evened-out" subset of the training data, and the ML code into one program. The training data is "evened-out" because that makes linearSVC more accurate: otherwise, that type of ML demonstrates a very strong bias towards whatever was most common in the training data.
Due to irregularities in the prediction code, sometimes multiple runs are necessary in order to return a reasonably accurate prediction.

URGENT TODO!!!
The ML algorithm scales the values for the training & test data. That's good, but we NEED TO FIGURE OUT HOW TO DO THAT SAME SCALING AGAIN. We can't just go scale(input) - it'll scale only relative to itself. There's got to be a way, of course--but what?
/URGENT TODO!!!
"""

from make_echonest_database import Song_data
import pickle
from sklearn import svm
from sklearn.metrics import confusion_matrix
import pprint
import requests
from pyechonest import config, song
import random

from pattern.en import sentiment # This was giving us some grief earlier. Might need to not use pattern.

from swampy.Gui import * # TODO: Check which swampy.Gui functions are actually needed/used. Importing * ain't ideal practice - it pollutes the namespace and often introduces tough-to-find bugs. It's fine here, but it's always good to practice good practice!

config.ECHO_NEST_API_KEY = "DCPW87SS20PQ4RXDR"

def get_lyrics(artist, title):
    url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]=' + artist + '%20' + title
    r = requests.get(url)
    r_text = r.text
    for (old, new) in [('false', 'False'), ('true', 'True'), ('null', 'None')]:
        r_text = r_text.replace(old, new)
    try:
        r_text_as_data = eval(r_text)
        if len(r_text_as_data) != 0:
            r_text_dict = r_text_as_data[0]
            return r_text_dict['snippet']
        else:
            return ''
    except:
        print 'lyrics failure'
        return ''


def get_data(artist, title):
    """
    Returns the parameters ['tempo', 'mode', . . . , 'energy'] for the song as a list, and the sentiment of the lyrics acc. pattern.
    These are given as a tuple: (parameter list, sentiment).
    """
    rkp_results = song.search(artist=artist, title=title) # Searches echonest for the song.
    if len(rkp_results) != 0: # length check
        current_song = rkp_results[0] # Takes the most likely match.
    else:
        print "Couldn't find " + artist + " : " + title + "."
        return -1
    lyrics = get_lyrics(artist, title)
    lyric_sentiment = sentiment(lyrics)[0] # should get a value between -1.0 and 1.0 for the sentiment
    current_song.audio_summary['sentiment'] = lyric_sentiment
    parameters = [current_song.audio_summary[k] for k in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy', 'sentiment']]
    return parameters
f = open('fifty_seven_years_database.txt', 'r')

song_database = pickle.load(f)

random.shuffle(song_database)

# moods_of_interest = ['Empowering', 'Upbeat', 'Excited', 'Sensual', 'Romantic', 'Urgent', 'Energizing', 'Cool', 'Rowdy', 'Brooding', 'Lively', 'Yearning', 'Sentimental']
# moods_of_interest = ['Empowering', 'Excited', 'Sensual', 'Romantic', 'Energizing', 'Cool', 'Brooding', 'Lively', 'Sentimental']
moods_of_interest = ['Empowering', 'Excited', 'Sensual', 'Energizing', 'Lively', 'Sentimental']


count_so_far = {k: 0 for k in moods_of_interest}

usable_songs = []

for i in song_database:
    if i.id != 'N/A':
        if i.mood1 != 'N/A' and i.mood1_text in moods_of_interest and i.parameter_dict['speechiness'] != None:
            if count_so_far[i.mood1_text] < 500:
                count_so_far[i.mood1_text] += 1
                usable_songs.append(i)

# print len(usable_songs)

parameters = [] # x-vals for training/testing
moodout = [] # corresponding y-vals for training/testing.

mood_to_int = {moods_of_interest[i]: i for i in range(len(moods_of_interest))}

for i in usable_songs:
    parameters.append([i.parameter_dict[k] for k in ['tempo', 'mode', 'key', 'danceability', 'acousticness', 'speechiness', 'loudness', 'energy','sentiment']])
    moodout.append(mood_to_int[i.mood1_text])

# from sklearn.preprocessing import scale
# parameters = scale(parameters) # svm isn't scale-insensitive, so pre-scaling it is handy.

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

parameters_train, parameters_test, moodout_train, moodout_test  = train_test_split(parameters, moodout, train_size=0.8)

val_counts = [moodout_train.count(i) for i in range(len(moods_of_interest))]

lin_clf = svm.SVC(kernel='linear', C=100000)

total_weight = sum([1.0/val_counts[v] for v in moodout_train])
lin_clf.fit(parameters_train, moodout_train, sample_weight=[1.0/val_counts[v]/total_weight for v in moodout_train])

prediction_list = []
accuracy = 0.0
for i in range(len(parameters_test)):
    prediction = lin_clf.predict(parameters_test[i])
    prediction_list.append(prediction)
    if prediction == moodout_test[i]:
        accuracy += 1.0/len(parameters_test)

accuracy = accuracy * 100
if accuracy <= 30:
    print("Accuracy too low, please run again")
print 'ACCURACY********'
print accuracy
print '-----------------'
if accuracy <= 30:
    print("Accuracy too low, please run again")

def get_food(artist, name):
    """
    TODO: Scale parameters. Get hot, cold, etc working properly. New dictionary might also be nice.
    """
    mood_to_food = {0: 'Steak', 1: 'Ice Cream', 2: 'a cannoli (nudge nudge wink wink)', 3: 'red bull jell-o', 4: 'Sashimi', 5: 'Grilled Cheese'}
    sd = get_data(artist, name)
    if sd == -1:
        return "Couldn't find " + artist + ' - ' + name
    predicted_mood = lin_clf.predict(sd)
    spiciness = sd[0] + sd[7]
    lyric_sentiment = sd[8]
    if lyric_sentiment > .33:
        a = 'Funfetti on '
    elif lyric_sentiment > 0:
        a = 'Cheese on '
    elif lyric_sentiment == 0:
        a = "Bowl o' "
    elif lyric_sentiment > -0.33:
        a = "Lukewarm hot fudge on "
    else:
        a = 'Tears on '
    if spiciness > 125:
        b = 'Hot '
    else:
        b = 'Cold '
    c = mood_to_food[predicted_mood[0]]
    return a+b+c
   
def show_food(artist, track):
    text = g.te(width=25, height=1)
    text.insert(END, get_food(artist, track))


if __name__ == "__main__":
    print '==========================\n========================='
    g = Gui()
    g.title('Funfetti Chicken')
    label = g.la(text='Enter a song and artist below')
    artist = g.en(text = 'Rick Astley')
    track = g.en(text = 'Never Gonna Give You Up')
    button = g.bu(text="Feed Me", command=lambda : show_food(artist.get(),track.get()))
    g.mainloop()
