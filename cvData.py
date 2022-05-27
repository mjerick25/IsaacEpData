import json
from tokenize import String
from pytube import YouTube
import os
import moviepy

testVids = []
with open("json/test_vids.json", "r") as test_file:
    testVids = json.load(test_file)
    test_file.close()

vidFileBaseDirectory = "D:/Northernlion2"
clipLength = 30

def getVideoFiles(video: dict, directory: String, clipLength: int):
    #If directory does not exist -> make it
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            print("Error making directory ", directory)
    
    #Create folder in directory
    #Format for folder name: version#number
    folderName = video["version"] + "#" + video["epNum"]
    folderDirectory = os.path.join(directory, folderName)

    #Ensures the folder does not already exist before creating it
    if not os.path.exists(folderDirectory):
        try:
            os.makedirs(folderDirectory)
        except:
            print("Error making folder ", folderDirectory)

    #Create our youtube object
    yt = YouTube(video["urL"])

    #Load in/download stream for video: lowest resolution
    #Lots of chaining here, but this loads in a 144p mp4 of the YouTube video and downloads it as folder/fullVideo.mp4
    videoDirectory = os.path.join(folderDirectory, "fullVideo.mp4")
    yt.streams.filter(res="144p", file_extension="mp4").first().download(folderDirectory, "fullVideo")
    
    #Load in/download stream for audio
    #Lots of chaining here, but this loads in an audio only mp4 of the video and downloads it as folder/fullAudio.mp4
    audioDirectory = os.path.join(folderDirectory, "fullVideo.mp4")
    yt.streams.filter(only_audio=True, file_extension="mp4").first.download(folderDirectory, "fullAudio")

    #Read in the downloaded video as a clip
    fullVidClip = VideoFileClip(videoDirectory, audio=False)
    #Create image sequence for first 30s
    #Written to directory/version#number/startSequence
    startSequenceDirectory = os.path.join(folderDirectory, "startSequence")
    if not os.path.exists(startSequenceDirectory):
        try:
            os.makedirs(startSequenceDirectory)
        except:
            print("Error making folder ", startSequenceDirectory)
    
    startClip = fullVidClip.subclip(0, clipLength)
    startClip.write_images_sequence(startSequenceDirectory + "/frame%03d.jpg")
    #Create image sequence for last 30s
    #Written to directory/version#number/endSequence
    endSequenceDirectory = os.path.join(folderDirectory, "endSequence")
    if not os.path.exists(endSequenceDirectory):
        try:
            os.makedirs(endSequenceDirectory)
        except:
            print("Error making folder ", endSequenceDirectory)

    endClip = fullVidClip.subclip(fullVidClip.duration - clipLength)
    endClip.write_images_sequence(endSequenceDirectory + "/frame%03d.jpg")
    
def findResult(video: dict, directory: String):
    #Goes to our video directory at directory/version#number/

def findSeedandCharacter() -> String:

def intro(video: dict, directory: String):
    #Goes to our video directory at directory/version#number

for vid in testVids:
    getVideoFiles(vid["urL"], "D:/Northernlion2/test_vids")