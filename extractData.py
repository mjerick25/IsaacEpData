from pytube import Playlist
from pytube import YouTube
from moviepy.editor import *
import constants
from skimage.metrics import structural_similarity as compare_ssim
import imutils
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

# Testing
testVids = boiPlaylist.videos[:5]
for i in range(1):
    vidData = videoData(testVids[i])

    videoDownload(testVids[1], vidData[1], vidData[0])
    eyyErybody(vidData[1], vidData[0])
    endClipToFrames(vidData[1], vidData[0])

    minScore = [1, 0]
    scores = np.zeros(900)
    for j in range(899):
        score = compareFrames(vidData[1], vidData[0], str(j), str(j+1))
        scores[j] = score
        if score < minScore[0]:
            minScore = [score, j]

    fig, ax = plt.subplots()
    ax.hist(scores, bins=100)
    plt.show()
    #Chart shows .5 and lower might be what we want to analyze
    print(minScore)
    print(i)



