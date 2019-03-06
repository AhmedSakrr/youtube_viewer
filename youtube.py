import requests
import json
from bs4 import BeautifulSoup

API_KEY = "AIzaSyANWCxvIiHvHqEpUO83INHwg05vHRaNLQw"
base_video_url = 'https://www.youtube.com/watch?v='
base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

channel_id = "UC_fsb-5q3QH-CXJ79YgrWfg"


class Video():
    def __init__(self, jsonObj):
        self.__dict__ = jsonObj['snippet']
        self.link = base_video_url + jsonObj['id']['videoId']
        self.properties = set(self.__dict__.keys())


def getChannelIdFromUser(user):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={user}&key={API_KEY}"
    source = requests.get(url).text
    sourceJson = json.loads(source)
    return sourceJson['items'][0]['id']


def getVideosFromUser(user, maxVids=10):
    videos = []

    channel_id = getChannelIdFromUser(user)
    first_url = base_search_url + \
        f'key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults={maxVids}'
    url = first_url
    while len(videos) < maxVids:
        source = requests.get(url).text
        sourceJson = json.loads(source)
        for i in sourceJson['items']:
            if i['id']['kind'] == "youtube#video":
                # print(i['snippet']['title'])
                videos.append(Video(i))

        """# Try to get next page
        try:
            next_page_token = sourceJson['nextPageToken']
            url = first_url + f'&pageToken={next_page_token}'
        except:
            break"""
    return videos


if __name__ == "__main__":
    videos = getVideosFromUser('szyzyg', 3)
    print(videos[0].properties)
    print()
    for v in videos:
        print(f"{v.publishedAt} - {v.title}\n{v.link}\n")
