import os
import requests
from datetime import datetime
from datetime import timezone
from PIL import Image

from flask import url_for
from viewer import app, db
from viewer.models import Video
from youtubeUtils import ytVideo

def utc_to_local(utc_dt_string):
    utc_dt = datetime.strptime(utc_dt_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return datetime.strftime(local_dt, "%Y-%m-%d %I:%M %p")

def downloadThumbnail(videoID):
    url = f"https://i.ytimg.com/vi/{videoID}/hqdefault.jpg"
    picture_path = os.path.join(app.root_path, 'static/thumbnails', f"{videoID}.jpg")
    if not os.path.exists(picture_path):
        print(f"Downloading image for video {videoID} at {url}")
        img_data = requests.get(url).content
        with open(picture_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Image for video {videoID} downloaded successfully")
    else:
        print(f"Image for video {videoID} already exists")
    return url_for('static', filename='thumbnails/' + videoID + ".jpg")

def downloadChannelImage(channelID, url):
    picture_path = os.path.join(app.root_path, 'static/thumbnails', f"{channelID}.jpg")
    if not os.path.exists(picture_path):
        print(f"Downloading image for channel {channelID} at {url}")
        img_data = requests.get(url).content
        with open(picture_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Image for channel {channelID} downloaded successfully")
    else:
        print(f"Image for channel {channelID} already exists")
    return url_for('static', filename='thumbnails/' + channelID + ".jpg")

def storeVideoInfoForChannel(channel):
    videoIDs = channel.videoIDs
    nVideosAdded = 0
    for videoID in videoIDs:
        if not Video.query.filter_by(videoID=videoID).first():
            v = ytVideo(videoID)
            thumbnail = downloadThumbnail(videoID)
            channelImg = downloadChannelImage(v.channelId, channel.img_url)
            video = Video(title=v.title, channelName=v.channelTitle, channelID=v.channelId, channelImg=channelImg, videoUrl=v.url, videoID=v.videoID, image=thumbnail, description=v.description, publishedAt=utc_to_local(v.publishedAt))
            db.session.add(video)
            nVideosAdded += 1
    db.session.commit()
    return nVideosAdded
