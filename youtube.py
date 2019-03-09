import requests
import json
from bs4 import BeautifulSoup

API_KEY = "AIzaSyCvJHk-N9s0sW5aP31d62tYgmHUSAi7FDI"

base_video_url = 'https://www.youtube.com/watch?v='
base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
base_channel_url = 'https://www.googleapis.com/youtube/v3/channels'


class ytVideo:
    def __init__(self, videoID):
        self.__dict__ = getVideoDetails(videoID)['snippet']
        self.videoID = videoID
        self.url = f"https://www.youtube.com/watch?v={self.videoID}"

    def __str__(self):
        output = ""
        for key in self.__dict__.keys():
            output += f"\n{key}: {self.__dict__[key]}\n"
        return output

class channelPlaylist:
    def __init__(self, user, maxResults=10):
        sourceObj = getUploadPlaylistFromUser(user, maxResults=maxResults)
        self.items = [sourceObj['items'][i]['contentDetails'] for i in range(len(sourceObj['items']))]
        self.videoObjects = []
        for item in self.items:
            self.videoObjects.append(ytVideo(item['videoId']))

    def __str__(self):
        output = ""
        for video in self.videoObjects:
            output += f"\n {video.videoID} - {video.publishedAt} \n"
        return output

def getUploadsIdFromUser(user):
    url = f"https://www.googleapis.com/youtube/v3/channels?forUsername={user}&key={API_KEY}&part=contentDetails"
    source = requests.get(url).text
    sourceJson = json.loads(source)
    uploadsID = sourceJson['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print(f"Found Uploads ID from user {user}: {uploadsID}")
    return uploadsID

def getUploadPlaylistFromUser(user, maxResults=10):
    uploadsID = getUploadsIdFromUser(user)
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={uploadsID}&maxResults={maxResults}&key={API_KEY}"
    source = requests.get(url).text
    sourceJson = json.loads(source)
    return sourceJson

def getVideoDetails(videoID):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={videoID}&key={API_KEY}"
    source = requests.get(url).text
    sourceJson = json.loads(source)['items'][0]
    return sourceJson


def getVideosFromUser(user, maxVids=10):
    videos = []

    playlistObj = getUploadPlaylistFromUser(user)

    return videos


if __name__ == "__main__":
    """
    videos = getVideosFromUser('szyzyg', 3)
    print(videos[0].properties)
    print()
    for v in videos:
        #print(f"{v.publishedAt} - {v.title}\n{v.link}\n")
        print(v)
    """
