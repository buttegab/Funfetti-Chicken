from pyechonest import config
config.ECHO_NEST_API_KEY="DCPW87SS20PQ4RXDR"

sad_foods = {1: 'tub of ice cream', 2:'bologna sandwich', 3: 'ramen noodles', 4: 'chicken broth', 5: 'hamburger helper', 6: 'frozen pizza'}
def find_song(artist, song_name):
	from pyechonest import song
	rkp_results = song.search(artist = artist, title = song_name)
	song = rkp_results[0]
	print song.audio_summary['tempo']
	print song.audio_summary['mode']
	print song.audio_summary['key']
	print song.audio_summary['danceability']
	print song.audio_summary['acousticness']
	print song.audio_summary['speechiness']


find_song('bob dylan', "like a rolling stone")