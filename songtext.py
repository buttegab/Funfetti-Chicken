import requests
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import math

artist = 'coldplay'
song = 'clocks'

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data



#url = 'http://developer.echonest.com/api/v4/song/search?api_key=3D2CNVOKTHG046F7R&format=json&artist=radiohead&title=creep&bucket=id:lyricfind-US&limit=true&bucket=tracks'
url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]=' + artist+ '%20'+ song
r = requests.get(url)
r_text = r.text
#print r["context"][0]
# print r_text

# r_text.replace()

r_text_pythonic = r_text.replace('false', 'False')
rtp = r_text_pythonic.replace('true', 'True')
rtp2 = rtp.replace('null', 'None')

r_text_as_list = eval(rtp2)
# print r_text_as_list

# print r_text_as_list[0]
test_dictionary = r_text_as_list[0]
print test_dictionary['snippet']
print test_dictionary['context']

test_dictionary = r_text_as_list[2]
print " "
print test_dictionary['snippet']

#test_dictionary = r_text_as_list[6]
#print test_dictionary['snippet']
#print test_dictionary['context']

#print test_dictionary['context']

# print type(r)
# r = 

#responsedata = get_json(url)
#print responsedata
"""readme:
Go to http://docs.python-requests.org/en/latest/user/install/ and do what it sayss to install requests.
Thats it.
This readme is essential.
"""