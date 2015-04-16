"""readme:
Go to http://docs.python-requests.org/en/latest/user/install/ and do what it sayss to install requests.
Thats it.
This readme is essential.
"""

import requests
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import math


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def get_lyrics(artist, song):
    """
    Gets lyrics for the given song, if it can be found in the lyricsnmusic api.
    -Matt
    """
    url = 'http://api.lyricsnmusic.com/songs?api_key=[5358b25688164e6c2f771954f17460&q]=' + artist+ '%20'+ song
    r = requests.get(url)
    r_text = r.text
    r_text = r_text.replace('false', 'False')
    r_text = r_text.replace('true', 'True')
    r_text = r_text.replace('null', 'None') # converting to something Python understands. These lines just replace 'true' with 'True', 'null' with 'None', etc--since java/c++/html/whatever language the api uses has *slightly* different syntax from python :P.
    r_text_as_data_structure = eval(r_text)
    if len(r_text_as_data_structure) != 0:
        r_text_dictionary = r_text_as_data_structure[0]
        return r_text_dictionary['snippet'] #returns a verse's worth of lyrics, which is all we can automatically get b/c copyright law in the APIs.
    else:
        return '' #means that nothing was found; as such, this is an empty string. This is to prevent a fatal error in the event that for some reason no song is found.

if __name__ == "__main__":
    print get_lyrics('Fall Out Boy', 'Immortals') # A test case, to see if the get_lyrics function is working.