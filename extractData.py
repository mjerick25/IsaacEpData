from pytube import Playlist
from pytube import YouTube
from moviepy.editor import *
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
    audioToDownload = vid.streams.get_audio_only()
    #Saves the mp4 to DOWNLOAD_PATH in a folder in the format version###
    folderName = version + epNumber
    videoFileName = folderName + ".mp4"
    #Separately downloads the audio from the video
    audioFileName = folderName + "audio.mp4"

    vidToDownload.download(output_path=constants.DOWNLOAD_PATH + "\\" + folderName, filename=videoFileName)
    audioToDownload.download(output_path = constants.DOWNLOAD_PATH + "\\" + folderName, filename=audioFileName)

def eyyErybody(version, epNumber):
    # Finds the location of the audio file for a given video
    audioFileFolder = constants.DOWNLOAD_PATH + "\\" + version + epNumber + "\\"
    audioFileName = version + epNumber + "audio.mp4"
    audioFileLocation = audioFileFolder + audioFileName

    # Loads in the whole audio clip
    audioClip = AudioFileClip(audioFileLocation)
    # Trims the audio clip to the first 2 seconds
    eyyErybodyClip = audioClip.subclip(0, 2)
    # Saves the audio clip to the folder for the corresponding video
    eyyErybodyClip.write_audiofile(audioFileFolder + "eyyerybody.wav", codec="pcm_s32le")
    audioClip.close()

def endClipToFrames(version, epNumber):
    folderName = constants.DOWNLOAD_PATH + "\\"+ version + epNumber
    videoFileName = version + epNumber + ".mp4"
    videoFileLocation = folderName + "\\" + videoFileName

    #Pulls the video clip in, removes last 30 seconds
    videoClip = VideoFileClip(videoFileLocation)
    videoEndClip = videoClip.subclip(videoClip.duration-30,videoClip.duration)

    #Saves 30 sec clip as image sequence (900?)
    os.makedirs(folderName + "\\imageSequence\\")
    videoEndClip.write_images_sequence(folderName + "\\imageSequence\\" + "frame%03d.png")

# Testing
testVids = boiPlaylist.videos[:5]
for i in range(5):
    vidData = videoData(testVids[i])

    videoDownload(testVids[1], vidData[1], vidData[0])
    eyyErybody(vidData[1], vidData[0])
    endClipToFrames(vidData[1], vidData[0])
    print(i)



