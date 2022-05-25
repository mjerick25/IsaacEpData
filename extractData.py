##DEPRECIATED FILE
#Replaced with vidData, createRandoms, cvData

from pytube import Playlist
from pytube import YouTube
from moviepy.editor import *
#import constants
from skimage.metrics import structural_similarity as compare_ssim
#import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np

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

    # Gets upload date
    uploadDateTime = vid.publish_date
    uploadMonth = uploadDateTime.strftime("%m")
    uploadDay = uploadDateTime.strftime("%d")
    uploadYear = uploadDateTime.strftime("%Y")
    uploadDate = uploadMonth + r"/" + uploadDay + r"/" + uploadYear

    # Finds video length, in seconds
    vidLength = vid.length

    return [epNumber, version, uploadDate, vidLength]


def videoDownload(vid, version, epNumber):
    # Downloads an mp4 version of the episode at 144p
    vidToDownload = vid.streams.filter(res="144p", subtype="mp4").first()
    audioToDownload = vid.streams.get_audio_only()
    # Saves the mp4 to DOWNLOAD_PATH in a folder in the format version###
    folderName = constants.DOWNLOAD_PATH + "\\" + version + epNumber
    videoFileName = version + epNumber + ".mp4"
    # Separately downloads the audio from the video
    audioFileName = version + epNumber + "audio.mp4"

    vidToDownload.download(output_path=folderName, filename=videoFileName)
    audioToDownload.download(output_path=folderName, filename=audioFileName)


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
    folderName = constants.DOWNLOAD_PATH + "\\" + version + epNumber + "\\"
    videoFileName = version + epNumber + ".mp4"
    videoFileLocation = folderName + videoFileName

    # Pulls the video clip in, takes in last 30 seconds
    videoClip = VideoFileClip(videoFileLocation)
    videoEndClip = videoClip.subclip(videoClip.duration-30, videoClip.duration)

    # Creates directory
    if not os.path.isdir(folderName + "\\imageSequence"):
        os.makedirs(folderName + "\\imageSequence\\")
    # Saves 30 sec clip as image sequence
    videoEndClip.write_images_sequence(folderName + "\\imageSequence\\" + "frame%d.png")
    #he uhhh do be closing
    videoClip.close()

def compareFrames(version, epNumber, frame1, frame2):
    # Finds the folder with the video as frames, takes 2 frames in
    folderName = constants.DOWNLOAD_PATH + "\\" + version + epNumber + "\\imageSequence\\"
    image1File = folderName + "frame" + frame1 + ".png"
    image2File = folderName + "frame" + frame2 + ".png"

    # Loads both images into cv2
    image1 = cv2.imread(image1File)
    image2 = cv2.imread(image2File)

    #
    image1gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    similarityScore = compare_ssim(image1gray, image2gray)

    return similarityScore

def analyzePotentialEnd(version, epNumber, frame):
    #if /endFrames/loss.png is found in image (up to certainty threshold)
    folderName = constants.DOWNLOAD_PATH + "\\" + version + epNumber + "\\imageSequence\\"
    frameName = "frame" + frame + ".png"
    frameLocation = folderName + frameName

    frameImage = cv2.imread(frameLocation, 0)

    lossFrameLocation = constants.DOWNLOAD_PATH + "\\endFrames\\loss.png"
    lossFrameImage = cv2.imread(lossFrameLocation, 0)

    avgLossScore = 0.0
    for meth in constants.MATCH_METHODS:
        methodInstance = eval(meth)
        res = cv2.matchTemplate(frameImage, lossFrameImage, methodInstance)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method == cv2.TM_SQDIFF_NORMED:
            lossScore = 1-min_val
        else:
            lossScore = max_val

        avgLossScore += lossScore

    avgLossScore = avgLossScore/len(constants.MATCH_METHODS)

    if(avgLossScore > constants.LOSS_THRESHOLD):
        return "loss - certainty: " + str(avgLossScore)

    #iterate through /endFrames/win/ to find most certain frame, win if above some threshold
    maxWinSimScore = 0
    maxWinSimImageName = ""
    for winCase in os.listdir(constants.DOWNLOAD_PATH + "\\endFrames\\wins\\"):
        winFrameImage = cv2.imread(constants.DOWNLOAD_PATH + "\\endFrames\\wins\\" + winCase, 0)
        winSimilarityScore = compare_ssim(frameImage, winFrameImage)

        if winSimilarityScore > maxWinSimScore:
            maxWinSimScore = winSimilarityScore
            maxWinSimImageName = winCase

    if maxWinSimScore > constants.WIN_THRESHOLD:
        winType = maxWinSimImageName[3:]
        return "win: " + winType + " - certainty: " + str(maxWinSimScore)

    #Neither of these catch
    return None

# Testing
testVids = boiPlaylist.videos[:5]

for i in range(1):
    vidData = videoData(testVids[i])

    videoDownload(testVids[1], vidData[1], vidData[0])
    eyyErybody(vidData[1], vidData[0])
    endClipToFrames(vidData[1], vidData[0])

    for j in range(899):
        score = compareFrames(vidData[1], vidData[0], str(j), str(j+1))
        if score < constants.FRAME_IMPORTANCE_THRESHOLD:
            print("Important frame found: " + str(j+1) + " - frame importance: " + str(score))
            potential = analyzePotentialEnd(vidData[1], vidData[0], str(j+1))
            if potential is not None:
                print(potential)
                break



