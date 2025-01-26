import json
import requests
from PIL import Image

f = open("data.json", "r")
lines = f.read()

jeson = json.loads(lines)

itemid = 0
for item in jeson["items"]:
    imglink = item["track"]["album"]["images"][0]["url"]
    print(imglink)

    data = requests.get(imglink).content

    filename = "images/image"+str(itemid)+".jpg"
    f = open(filename, 'wb')

    f.write(data)
    f.close()

    itemid += 1