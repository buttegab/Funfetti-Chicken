"""
Funfetti Chicken
SoftDes Spring 2015

"""
from pattern.en import *
import requests
from pyechonest import config
config.ECHO_NEST_API_KEY="DCPW87SS20PQ4RXDR"
from pyechonest import song

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data

# User inputs.
#artist = raw_input("Please enter an artist: ")
#title = raw_input("Please enter an title: ")
artist='coldplay'
title='clocks'

# Song search
rkp_results = song.search(artist=artist,title=title)
song = rkp_results[0]

#Get lyrics
url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]='+artist+'%20'+title
r = requests.get(url)
r_text = r.text

#Clean lyrics
r_text_pythonic = r_text.replace('false', 'False')
rtp = r_text_pythonic.replace('true', 'True')
rtp2 = rtp.replace('null', 'None')
r_text_as_list = eval(rtp2)

test_dictionary = r_text_as_list[0]

p1 = test_dictionary['snippet']
p2 = test_dictionary['context']

test_dictionary = r_text_as_list[2]
p3 = test_dictionary['snippet']

#Check food dictionary
#print p1+p2+''+p3

#Analize lyrics sentiments
sentiment = sentiment(p1+p2+''+p3)
print 'Lyrics: ',sentiment

#Exact information about the song
#print song.artist_location

print 'Energy:',song.audio_summary['energy']
print 'Tempo:',song.audio_summary['tempo']
print 'Mode:',song.audio_summary['mode']
print 'Key:',song.audio_summary['key']
print 'Valence:',song.audio_summary['valence']
print 'Loudness:',song.audio_summary['loudness']

#print 'liveness:',song.audio_summary['liveness']
#print 'acousticness:' ,song.audio_summary['acousticness']
#print 'speechiness:',song.audio_summary['speechiness']
#print 'time_signature:',song.audio_summary['time_signature']
#print 'danceability:',song.audio_summary['danceability']
