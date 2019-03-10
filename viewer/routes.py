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
    print(f"Downloading image for {videoID} at {url}")
    img_data = requests.get(url).content
    with open(picture_path, 'wb') as handler:
        handler.write(img_data)
    print(f"Image for {videoID} downloaded successfully")
    return url_for('static', filename='thumbnails/' + videoID + ".jpg")

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    #videos = Video.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        print("VALIDATED")
        videoIDs = channelPlaylist(form.channelName.data, maxResults=form.maxResults.data).videoIDs
        nVideosAdded = 0
        for videoID in videoIDs:
            if not Video.query.filter_by(videoID=videoID).first():
                v = ytVideo(videoID)
                thumbnail = downloadThumbnail(videoID)
                video = Video(title=v.title, channelName=v.channelTitle, videoUrl=v.url, videoID=v.videoID, image=thumbnail,description=v.description, publishedAt=utc_to_local(v.publishedAt))
                db.session.add(video)
                nVideosAdded += 1
            else:
                print(Video.query.filter_by(videoID=videoID).first().image)
        db.session.commit()
        print(f"ADDED {nVideosAdded} VIDEO(S) TO DATABASE")
        return redirect(url_for('results'))

    return render_template('home.html', form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    videos = Video.query.all()
    return render_template('results.html', videos=videos)
