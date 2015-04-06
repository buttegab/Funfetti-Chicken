import requests

artist = 'coldplay'
song = 'clocks'

url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]=' + artist+ '%20'+ song
r = requests.get(url)
print r.text

"""readme:
Go to http://docs.python-requests.org/en/latest/user/install/ and do what it sayss to install requests.
Thats it.
This readme is essential.
"""