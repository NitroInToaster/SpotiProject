import requests
import json

ile = 2000 #ile piosenek chcemy
tyle = 0 #pomocnicze

request = 'https://api.spotify.com/v1/playlists/1OANCp8xc0IjAbPeijbwek/tracks?fields=items%28track%28name%2C+artists%28id%29+%2Calbum%28images%28url%29%29%29%29&limit=100&offset='+str(tyle)

playlistjson = requests.get(request, headers = {"Authorization" : header}).text[0:-2] + ','
tyle += 100

while tyle < ile-100:
    request = 'https://api.spotify.com/v1/playlists/1OANCp8xc0IjAbPeijbwek/tracks?fields=items%28track%28name%2C+artists%28id%29+%2Calbum%28images%28url%29%29%29%29&limit=100&offset='+str(tyle)
    
    playlistjson = playlistjson + requests.get(request, headers = {"Authorization" : header}).text[10:-2] + ','
    tyle += 100

request = 'https://api.spotify.com/v1/playlists/1OANCp8xc0IjAbPeijbwek/tracks?fields=items%28track%28name%2C+artists%28id%29+%2Calbum%28images%28url%29%29%29%29&limit=100&offset='+str(tyle)

playlistjson = playlistjson + requests.get(request, headers = {"Authorization" : header}).text[10:]
tyle += 100

print(playlistjson)

# now write output to a file
with open("data.json", "w") as DataFile:
    # magic happens here to make it pretty-printed
    DataFile.write(
        json.dumps(json.loads(playlistjson), indent=1, sort_keys=True)
    )
