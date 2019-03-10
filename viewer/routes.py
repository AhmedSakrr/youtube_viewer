import os
import sys
sys.path.append('..')

from PIL import Image
from datetime import datetime
from datetime import timezone
from flask import render_template, url_for, flash, redirect, request
from viewer import app, db
from viewer.forms import SearchForm #RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from viewer.models import Video #User, Post
#from flask_login import login_user, current_user, logout_user, login_required
from youtube import *

global videos
videos = []

def utc_to_local(utc_dt_string):
    utc_dt = datetime.strptime(utc_dt_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return datetime.strftime(local_dt, "%Y-%m-%d %I:%M %p")

def downloadThumbnail(videoID):
    url = f"https://i.ytimg.com/vi/{videoID}/hqdefault.jpg"
    picture_path = os.path.join(app.root_path, 'static/thumbnails', f"{videoID}.jpg")
    print(f"Downloading image for video {videoID} at {url}")
    img_data = requests.get(url).content
    with open(picture_path, 'wb') as handler:
        handler.write(img_data)
    print(f"Image for video {videoID} downloaded successfully")
    return url_for('static', filename='thumbnails/' + videoID + ".jpg")

def downloadChannelImage(channelID, url):
    picture_path = os.path.join(app.root_path, 'static/thumbnails', f"{channelID}.jpg")
    if not os.path.exists(picture_path):
        print(f"Downloading image for channel {channelID} at {url}")
        img_data = requests.get(url).content
        with open(picture_path, 'wb') as handler:
            handler.write(img_data)
        #output_size = (10, 10)
        #i = Image.open(picture_path)
        #i.thumbnail(output_size)
        #i.save(picture_path)
        print(f"Image for channel {channelID} downloaded successfully")
    else:
        print(f"Image for channel {channelID} already exists")
    return url_for('static', filename='thumbnails/' + channelID + ".jpg")

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    #videos = Video.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        channel = channelPlaylist(form.channelName.data, maxResults=form.maxResults.data, isUser=form.isUser.data)
        print(channel.img_url)
        videoIDs = channel.videoIDs
        nVideosAdded = 0
        for videoID in videoIDs:
            if not Video.query.filter_by(videoID=videoID).first():
                v = ytVideo(videoID)
                thumbnail = downloadThumbnail(videoID)
                channelImg = downloadChannelImage(v.channelId, channel.img_url)
                video = Video(title=v.title, channelName=v.channelTitle, channelID=v.channelId, channelImg=channelImg, videoUrl=v.url, videoID=v.videoID, image=thumbnail,description=v.description, publishedAt=utc_to_local(v.publishedAt))
                db.session.add(video)
                nVideosAdded += 1
            else:
                print(Video.query.filter_by(videoID=videoID).first().image)
        db.session.commit()
        channelID = Video.query.filter_by(videoID=videoIDs[0]).first().channelID
        print(f"ADDED {nVideosAdded} VIDEO(S) TO DATABASE")
        return redirect(url_for('channel', channelID=channelID))

    knownChannels = [{'channelName':v.channelName, 'channelID':v.channelID, 'channelImg':v.channelImg} for v in Video.query.group_by(Video.channelName)]
    return render_template('home.html', form=form, knownChannels=knownChannels)

@app.route("/results", methods=['GET', 'POST'])
def results():
    videos = Video.query.all()
    return render_template('results.html', videos=videos)

@app.route("/channel/<channelID>")
def channel(channelID):
    videos = Video.query.filter_by(channelID=channelID).all()
    return render_template('results.html', videos=videos)
