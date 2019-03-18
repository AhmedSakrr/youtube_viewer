import requests
import json
from bs4 import BeautifulSoup
import pprint
import string

from ytapi import API_KEY

pp = pprint.PrettyPrinter(indent=4)



base_video_url = 'https://www.youtube.com/watch?v='
base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
base_channel_url = 'https://www.googleapis.com/youtube/v3/channels'


class ytVideo:
    def __init__(self, videoID):
        self.__dict__ = getVideoDetails(videoID)['snippet']
        self.videoID = videoID
        self.url = f"https://www.youtube.com/watch?v={self.videoID}"
        self.image = f"https://i.ytimg.com/vi/{self.videoID}/hqdefault.jpg"

    def __str__(self):
        output = ""
        for key in self.__dict__.keys():
            output += f"\n{key}: {self.__dict__[key]}\n"
        return output

class channelPlaylist:
    def __init__(self, identifier, maxResults=10):
        self.sourceObj, self.img_url = getUploadPlaylist(identifier, maxResults=maxResults)
        self.items = [self.sourceObj['items'][i]['contentDetails'] for i in range(len(self.sourceObj['items']))]
        self.videoIDs = []
        for item in self.items:
            self.videoIDs.append(item['videoId'])

    def __str__(self):
        output = ""
        for videoID in self.videoIDs:
            output += f"\n {videoID} \n"
        return output


def isUser(identifier):
    identifier = set(identifier)
    invalidUserChars = string.punctuation
    return not any(char in invalidUserChars for char in identifier)

def getUploadsIdFromUser(user):
    url = f"https://www.googleapis.com/youtube/v3/channels?forUsername={user}&key={API_KEY}&part=contentDetails,snippet"
    source = requests.get(url).text
    sourceJson = json.loads(source)
    uploadsID = sourceJson['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    img_url = sourceJson['items'][0]['snippet']['thumbnails']['default']['url']
    print(f"Found Uploads ID from user {user}: {uploadsID}")
    return uploadsID, img_url

def getUploadsIdFromChannelID(channelID):
    url = f"https://www.googleapis.com/youtube/v3/channels?id={channelID}&key={API_KEY}&part=contentDetails,snippet"
    source = requests.get(url).text
    sourceJson = json.loads(source)
    uploadsID = sourceJson['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    img_url = sourceJson['items'][0]['snippet']['thumbnails']['default']['url']
    print(f"Found Uploads ID from channelID {channelID}: {uploadsID}")
    return uploadsID, img_url

def getUploadPlaylist(identifier, maxResults=10):
    is_user = isUser(identifier)
    if is_user:
        uploadsID, img_url = getUploadsIdFromUser(identifier)
    else:
        uploadsID, img_url = getUploadsIdFromChannelID(identifier)
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={uploadsID}&maxResults={maxResults}&key={API_KEY}"
    source = requests.get(url).text
    sourceJson = json.loads(source)
    return sourceJson, img_url

def getVideoDetails(videoID):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={videoID}&key={API_KEY}"
    source = requests.get(url).text
    sourceJson = json.loads(source)['items'][0]
    return sourceJson


if __name__ == "__main__":
    import time
    test_string = 'UC_fsb-5q3QH-CXJ79YgrWfg'
    N = 1000000
    t_start = time.perf_counter()
    for i in range(N):
        print(isUser(test_string))
    t_end = time.perf_counter()
    t1 = t_end - t_start

    t_start = time.perf_counter()
    for i in range(N):
        print(isUser2(test_string))
    t_end = time.perf_counter()
    t2 = t_end - t_start

    print(f"isUser  ran in {1000*t1} milliseconds")
    print(f"isUser2 ran in {1000*t2} milliseconds")
