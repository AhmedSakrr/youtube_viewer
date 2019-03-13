import requests
import json
from bs4 import BeautifulSoup
import pprint

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
    def __init__(self, identifier, maxResults=10, isUser=True):
        self.sourceObj, self.img_url = getUploadPlaylist(identifier, maxResults=maxResults, isUser=isUser)
        self.items = [self.sourceObj['items'][i]['contentDetails'] for i in range(len(self.sourceObj['items']))]
        self.videoIDs = []
        for item in self.items:
            self.videoIDs.append(item['videoId'])

    def __str__(self):
        output = ""
        for videoID in self.videoIDs:
            output += f"\n {videoID} \n"
        return output

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

def getUploadPlaylist(identifier, isUser=True, maxResults=10):
    if isUser:
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
    uploads = getUploadsIdFromUser('hellogreedo')
    pp.pprint(uploads)
