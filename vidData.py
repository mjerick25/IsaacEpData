from pytube import Playlist
from pytube import YouTube
from datetime import date
import json

def populateData(list: list, playlist: Playlist):
    videos = playlist.videos
    for vid in videos:
        title = "unknown"
        version = "unknown"
        epNum = -1
        epDate = vid.publish_date.strftime("%m/%d/%y")
        print(epDate)
        duration = vid.length
        url = vid.embed_url

        #Used a lot
        vidName = vid.title.lower()

        # Find our title:
        #If we find a [, save the index of it and find the title that way
        if (idx := vidName.find("[")) != -1:
            title = vid.title[idx+1:vidName.find("]", idx)]

        # Find our version:
        if("repentance" in vidName):
            #repentance
            version = "repentance"
        elif("afterbirth" in vidName):
            if("afterbirth+" in vidName):
                version = "afterbirth+"
                #AB+
            else:
                version = "afterbirth"
                #AB
        elif("antibirth" in vidName):
            #antibirth
            version = "antibirth"
        else:
            #rebirth
            version = "rebirth"
        
        # Find our episode number:
        vidName = vidName.replace(":", "")
        vidName = vidName.replace("-", "")
        if(len(numbers := [s for s in vidName.split() if s.isdigit()]) != 1):
            #Could occur if there is no episode number in title, or if a number is somewhere else
            print("Problem Reading Ep # of Episode: " + vidName)
        else:
            epNum = numbers[0]

        tempData = {"title": title, "version": version, "epNum": epNum, "date": epDate, "duration": duration, "urL":url}
        list.append(tempData)


rebirthPlaylist = Playlist("https://www.youtube.com/playlist?list=PL1O4GjhJgk43b5B8zyOykepr6PCWo6xBq")
antibirthPlaylist = Playlist("https://www.youtube.com/playlist?list=PL1O4GjhJgk43m7oAkq8kDyVIenUwPohc4")
afterbirthPlaylist = Playlist("https://www.youtube.com/playlist?list=PL1bauNEiHIgxMmZpra5SAuzqr0yyPwNI2")
abplusRepentancePlaylist = Playlist("https://www.youtube.com/playlist?list=PL1bauNEiHIgwWzA2cOTeTW-nZeWsH7JPH")
vidData = []

with open('json/vid_data.json', 'r') as file:
    vidData = json.load(file)
    file.close()

try:
    populateData(vidData, abplusRepentancePlaylist)
except:
    print("Failure!")
    with open('json/vid_data.json', 'w') as file:
        json.dump(vidData, file)
        file.close()


with open('json/vid_data.json', 'w') as file:
    json.dump(vidData, file)
    file.close()