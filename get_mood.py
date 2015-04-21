import json
import urllib2 
import pygn
userID = '27678235334765580-1FB57EBF64483B1937D128ACEB314A68'

def get_mood(artist, name):
	artist = str(artist)
	title = str(name)
	data = pygn.search(clientID='10189056-547D2643844BF1E2B9E85BD85773AEFE', userID=userID, artist=artist, track=title)
	return data['mood']
	#['response']['songs'][0]['id']

print userID
print get_mood('bob dylan', 'like a rolling stone')
