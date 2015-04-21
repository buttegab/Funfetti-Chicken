import json
<<<<<<< HEAD
import urllib2 
import pygn
userID = '27678235334765580-1FB57EBF64483B1937D128ACEB314A68'

def get_mood(artist, name):
	artist = str(artist)
	title = str(name)
	data = pygn.search(clientID='10189056-547D2643844BF1E2B9E85BD85773AEFE', userID=userID, artist=artist, track=title)
	return data['mood']
=======
import urllib2

def get_mood():
	title = 'creep'
	url = "http://api.rovicorp.com/data/v1.1/song/info?track=yellow&include=moods&country=US&language=en&format=json&apikey=swcmmx3zb3xtm2avdctmzxrz&sig=NN2UdzbJPf"
	#'http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year/top-100-songs-1950.html'
	#str('http://developer.echonest.com/api/v4/song/search?api_key=DCPW87SS20PQ4RXDR&format=json&results=1&artist=radiohead&title='+title)
	#"http://api.rovicorp.com/data/v1.1/song/info?track=yellow&country=US&language=en&format=json&apikey=a4779rmf2wq6h9w4af6hryzh&sig=890aca71f1beff8562793e1c170ce4c2"
	data = json.load(urllib2.urlopen(url))
	return data
>>>>>>> 9aee4099a36ab93361fab6234e70598e830c88ae
	#['response']['songs'][0]['id']

print userID
print get_mood('bob dylan', 'like a rolling stone')
