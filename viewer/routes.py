import os
import sys
sys.path.append('..')
from PIL import Image
from datetime import datetime
from datetime import timezone
from flask import render_template, url_for, flash, redirect, request
from viewer import app, db
from viewer.forms import MySearchForm #RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from viewer.models import Video #User, Post
#from flask_login import login_user, current_user, logout_user, login_required
from youtube import *

global videos
videos = []

def utc_to_local(utc_dt_string):
    utc_dt = datetime.strptime(utc_dt_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return datetime.strftime(local_dt, "%Y-%m-%d %I:%M %p")

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    #videos = Video.query.all()
    form = MySearchForm()
    if form.validate_on_submit():
        print("VALIDATED")
        videos = channelPlaylist(form.channelName.data, maxResults=form.maxResults.data).videoObjects
        for v in videos:
            if not Video.query.filter_by(title=v.title).first():
                video = Video(title=v.title, channelName=v.channelTitle, videoUrl=v.url, description=v.description, publishedAt=utc_to_local(v.publishedAt))
                db.session.add(video)
        db.session.commit()
        return redirect(url_for('results'))
    else:
        print(form.channelName.data)
        print("form did not validate")

    return render_template('home.html', form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    videos = Video.query.all()
    return render_template('results.html', videos=videos)
