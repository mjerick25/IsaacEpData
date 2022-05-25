import json
from tokenize import String
from pytube import YouTube

testVids = []
with open("json/test_vids.json", "r") as test_file:
    testVids = json.load(test_file)
    test_file.close()

def getVideoFiles(video: dict, directory: String):
    #If directory does not exist -> make it

    #Create folder in directory
    #Format for folder name: version#number

    #Create our youtube object

    #Load in/download stream for video: lowest resolution

    #Load in/download stream for audio

    #Create image sequence for first 30s
    #Written to directory/version#number/startSequence

    #Create image sequence for last 30s
    #Written to directory/version#number/endSequence

def findResult(video: dict, directory: String):
    #Goes to our video directory at directory/version#number/

def findSeedandCharacter() -> String:

def intro(video: dict, directory: String):
    #Goes to our video directory at directory/version#number

for vid in testVids:
    getVideoFiles(vid["urL"], "D:/Northernlion2/test_vids")