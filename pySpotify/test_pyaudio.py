#verification of python - spotify script 
# Erase cache and prompt for user permission
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time


username = 'zack_manesiotis'
scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-private playlist-modify-private'
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = 'http://apple.com/'


try:
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    # token = util.prompt_for_user_token(username,scope)
except(AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    # token = util.prompt_for_user_token(username,scope)
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)


# Create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

# Get current device
devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']



# Current track information
track = spotifyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()

# artist = track['artists']['items'][0]
# track = track['item']['name']
 
# if artist != "":
#     print("Currently playing " + artist + " - " + track)


# User information
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(">>> Welcome to Spotipy " + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("1 - Search for a song")
    print("0 - Exit")
    print()
    choice = input("Your choice: ")

    # Search for the artist
    if choice == "1":
        print()
        searchQuery = input("Artist's Name: ")
        print()

        # Get search results
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        #webbrowser.open(song['images'][0]['url'])
        artistID = artist['id']


        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        # See album art
        while True:
            songSelection = input("Enter a song number to see album art and play the song (x to exit): ") # and play the song
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            spotifyObject.start_playback(deviceID, None, trackSelectionList) # added
            webbrowser.open(trackArt[int(songSelection)]) 

            List = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 203, 202, 203, 202, 202, 202, 302, 202, 302, 202]
            #volume = spotifyObject.volume(0)
            volume = spotifyObject.volume(0)
            while True:
                for i in range(len(List)): 
                    if (0 <= List[i] <= 100):
                        #it is from the volume sensor
                        volume = spotifyObject.volume(List[i])
                        print("Changing the volume")
                        time.sleep(1)
                    elif List[i] == 202:
                        #it is from gesture control 
                        if List[i-1] == 203: 
                            #hand swiped from left to right, so skip right
                            spotifyObject.pause_playback(deviceID)
                            print("pause")
                           # webbrowser.open(trackArt[int(songSelection)])
                            time.sleep(2)
                        if List[i-1] == 302: 
                            spotifyObject.start_playback(deviceID)
                            print("play")
                            #webbrowser.open(trackArt[int(songSelection)])
                            time.sleep(2)
                        
                        

                    else:  
                        #do nothing 
                        print("did not receive data")
                break; 


            if choice == "0":
                break


