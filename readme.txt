Project Funfetti Chicken
Matching Music to Sentiment, and Sentiment to Food.

Olin College, Software Design Spring 2015.

EXPLANATION:

(0) print_some_songs.py, find_tempo.py, drafts.py, Code_Review_prep_and_framing.txt,pseudocode are old tests, and can be safely ignored.

(0.1) database_cleaner.py currently does nothing of interest; it will be integrated once the mood-finding is up and running.

(1) get_a_bunch_of_songs.py is a script which only needs to be run once. It uses the internet to generate a huge list of recently-popular songs, which it then stores in billboard_song_list.txt

(1.1) billboard_song_list.txt is a text file which contains a list of pickled (artist, song_name) tuples from Billboard.

(2) songtext.py contains a function to get the lyrics from a song. It is used as part of the Song_data object's initialization function.

(3) make_echonest_database.py establishes the Song_data class. When a Song_data object is initialized, with artist & name as its parameters, it automatically calls echonest api to get things like 'tempo' and 'key.' This info then gets stored as parameters for this object. Additionally, the object also stores lyrics gotten from (2).

(4) wrapper.py is a wrapper. It uses the list from (1) and the class from (3), and then makes a big database of Song_data objects - one for every entry in the list of songs. This then gets pickled for later use, under song_database.txt.

(4.1) song_database.txt is a file containing a list of pickled Song_data objects. In other words, it's a big list of objects which have things like 'name', 'artist', 'mood,' 'lyrics,' etc. as parameters.

-M