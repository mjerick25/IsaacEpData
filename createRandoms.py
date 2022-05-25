import json
import random

vidData = []

with open('json/vid_data.json', 'r') as file:
    vidData = json.load(file)
    file.close()

print(len(vidData))
#Create our set of testing videos
testVids = []
for i in range(50):
    testVids.append(vidData[random.randint(0, len(vidData))])

with open('json/test_vids.json', 'w') as file:
    json.dump(testVids, file)
    file.close()