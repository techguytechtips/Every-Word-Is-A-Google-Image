from googleapiclient.errors import HttpError
import lyricsgenius
from google_images_search import GoogleImagesSearch
from datetime import datetime
import pytz
import os
from shutil import copyfile
#TODO might be a better way of doing this later
googletoken = open("GoogleToken.txt", "r").read().split()
geniustoken = open("GeniusToken.txt", "r")
gAPI = GoogleImagesSearch(googletoken[0], googletoken[1])
genius = lyricsgenius.Genius(geniustoken.read())
def getLyrics():
    artistInput = input("Please Enter Artist: ")
    songInput = input("Please Enter Song: ")
    #Remove the Section Headers so it doesn't search it
    genius.remove_section_headers = True
    #Search for the artists songs
    artist = genius.search_artist(artistInput, max_songs=1, sort="title")
    #Search for the song
    song = genius.search_song(songInput, artist.name)
    #Turn the Genius string into a array
    try: 
        songarray = (song.lyrics).split()
    except AttributeError:
        print("Failed to retrieve lyrics. This is caused by a bug in the lyricsgenius library, please retry.")
    return songarray
        
def ImgSearch():
    songarray = getLyrics()
    if not os.path.exists("ImageCache"):
        os.makedirs("ImageCache")
    if not os.path.exists("Images"):
        os.makedirs("Images")
    #Make a Index number that it can increase every time in the loop
    i = 0
    def GSearch():
        gAPI.search(search_params=_search_params, path_to_dir="ImageCache", custom_image_name=str(i))
        try:
            if str(open("ImageCache/" + str(i) + ".jpg",'rb').read(4)) != "b'\\xff\\xd8\\xff\\xe0'":
                print("Image is corrupt, Using Backup")
                copyfile("ImageCache/" + str(i) + "(1).jpg", "Images/" + str(i) + ".jpg" )
                os.remove("ImageCache/" +  str(i) + ".jpg")
            else:
                copyfile("ImageCache/" + str(i) + ".jpg", "Images/" + str(i) + ".jpg" )
        except FileNotFoundError as fnfe:
            print(fnfe)
            GSearch()
            
    #Google Image Search Parameters
    _search_params = {
        #Search for each word in songarray
        'q': songarray[i],
        #Image Type
        'fileType': 'jpg',
        'imgType': 'photo',
        #How many images to Download per word (This will not effect how many words you can download until you pass 10 images.)
        'num': 2,
    }
    #TODO turn for loop into while loop for non wasted memory
    for word in songarray:
        _search_params['q'] = songarray[i]
        #Tell user what word is being searched for 
        print("Now searching for Number " + str(i) + " " + songarray[i])
        #Search!
        try:
            GSearch()
        except HttpError as e:
            print(e)
            #The Quota Resets at 12:00 AM PST
            #Wait until 1 minute past 12:00 AM PST to continue 
            print("Maximum ammount of queries reached.")
            print("Waiting until 00:01:00 PST To Continue.")
            #While loop to continuely check the time until it reaches the desired time
            #TODO change While True
            while True:
                time = datetime.now(pytz.timezone('US/Pacific')).strftime("%H:%M:%S")
                if time == ("00:01:00"):
                    print("The Query Limit Has Reset, Continuing.")
                    GSearch()
                    break
        i += 1
ImgSearch()