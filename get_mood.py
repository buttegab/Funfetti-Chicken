import json
import urllib2 

def get_mood():
	title = 'creep'
	url = "http://api.rovicorp.com/data/v1.1/song/info?track=yellow&include=moods&country=US&language=en&format=json&apikey=g6mj4hxhrs5na3827sj6bygx&sig=42e988e601a1f909d7af968a007337a5"
	#'http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year/top-100-songs-1950.html'
	#str('http://developer.echonest.com/api/v4/song/search?api_key=DCPW87SS20PQ4RXDR&format=json&results=1&artist=radiohead&title='+title)
	#"http://api.rovicorp.com/data/v1.1/song/info?track=yellow&country=US&language=en&format=json&apikey=a4779rmf2wq6h9w4af6hryzh&sig=890aca71f1beff8562793e1c170ce4c2"
	data = json.load(urllib2.urlopen(url))
	return data
	#['response']['songs'][0]['id']

print get_mood()
