import json
import requests


f = open("data.json", "r")
lines = f.read()

jeson = json.loads(lines)

#rint(jeson["items"][2])
itemid = 0
for item in jeson["items"]:
    artistid = item["track"]["artists"][0]['id']
    print(artistid)
    request = 'https://api.spotify.com/v1/artists/'+artistid

    artistresp = requests.get(request, headers = {"Authorization" : header})

    artistjson = json.loads(artistresp.text)

    if artistjson["genres"] != []:
        genre = artistjson["genres"][0]
        print(genre)
        jeson["items"][itemid]["track"]["genre"] = genre
    itemid += 1

r = json.dumps(jeson)

with open("data.json", "w") as DataFile:
    # magic happens here to make it pretty-printed
    DataFile.write(
        json.dumps(json.loads(r), indent=1, sort_keys=True)
    )
