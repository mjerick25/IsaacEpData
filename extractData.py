from pytube import Playlist
from pytube import YouTube
import constants
from datetime import datetime

boiPlaylist = Playlist(constants.ISAAC_PLAYLIST)

def videoData(vid):
    # ensures what is passed in is a YouTube object
    if type(vid) != YouTube:
        print("Invalid parameter passed into VideoData()")
        return None

    # Takes the entire video title from the given video
    title = vid.title

    # Searches for the episode number in the title
    epNumber = ""
    for char in title:
        if char.isdigit():
            epNumber += char

    # Searches for isaac version
    if "rebirth" in title.lower():
        version = "Rebirth"
    if "repentance" in title.lower():
        version = "Repentance"
    if "afterbirth" in title.lower():
        if "afterbirth+" in title.lower():
            version = "Afterbirth Plus"
        else:
            version = "Afterbirth"

    #Gets upload date
    uploadDateTime = vid.publish_date
    uploadMonth = uploadDateTime.strftime("%m")
    uploadDay = uploadDateTime.strftime("%d")
    uploadYear = uploadDateTime.strftime("%Y")
    uploadDate = uploadMonth + r"/" + uploadDay + r"/" + uploadYear

    #Finds video length, in seconds
    vidLength = vid.length

    return [epNumber, version, uploadDate, vidLength]


def videoDownload(vid, version, epNumber):
    #Downloads an mp4 version of the episode at 144p
    vidToDownload = vid.streams.filter(res="144p", subtype="mp4").first()
    #Saves the mp4 to DOWNLOAD_PATH in a folder in the format version###
    folderName = version + epNumber
    fileName = folderName + ".mp4"
    vidToDownload.download(output_path=constants.DOWNLOAD_PATH + "\\" + folderName, filename=fileName)




