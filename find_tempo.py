"""
...pretty sure this was just a test file? -M
"""

from pyechonest import config
config.ECHO_NEST_API_KEY="NOLYZICKJ6J3JQ7LS"

sad_foods = {1: 'tub of ice cream', 2:'bologna sandwich', 3: 'ramen noodles', 4: 'chicken broth', 5: 'hamburger helper', 6: 'frozen pizza'}
def find_song(artist, song_name):
	from pyechonest import song # Re-importing ain't the most efficient, computation-wise.
	rkp_results = song.search(artist = artist, title = song_name)
	# print rkp_results
	cs = rkp_results[0] # Overloading variables (e.g.: importing the "song" module and creating a "song" variable) isn't... ideal practice. Some packages, languages, etc. are less forgiving than Python.
	print cs.audio_summary['tempo']
    # print song.artist_id
 #    # print song.
	# print song.audio_summary['tempo']
	# print song.audio_summary['mode']
	# print song.audio_summary['key']
	# print song.audio_summary['danceability']
	# print song.audio_summary['acousticness']
	# print song.audio_summary['speechiness']
	# print song.audio_summary
	# print song.audio_summary['track_id']


find_song('bob dylan', "like a rolling stone")