import os
import sys
sys.path.append('..')

from flask import render_template, url_for, flash, redirect, request
from viewer import app, db
from viewer.forms import SearchForm #RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from viewer.models import Video #User, Post
#from flask_login import login_user, current_user, logout_user, login_required
from viewer.serverUtils import utc_to_local, downloadThumbnail, downloadChannelImage, storeVideoInfoForChannel
from youtubeUtils import channelPlaylist

#global videos
#videos = []


def deleteThumbnail(identifier):
    image_path = os.path.abspath(f"viewer/static/thumbnails/{identifier}.jpg")
    if os.path.isfile(image_path):
        print(f"DELETING {image_path}")
        os.remove(image_path)
    else:
        pass

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    #videos = Video.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        channel = channelPlaylist(form.channelName.data, maxResults=form.maxResults.data, isUser=form.isUser.data)
        videoIDs = channel.videoIDs
        nVideosAdded = storeVideoInfoForChannel(channel)
        channelID = Video.query.filter_by(videoID=videoIDs[0]).first().channelID
        print(f"ADDED {nVideosAdded} VIDEO(S) TO DATABASE")
        return redirect(url_for('channel', channelID=channelID))

    knownChannels = [{'channelName':v.channelName, 'channelID':v.channelID, 'channelImg':v.channelImg} for v in Video.query.group_by(Video.channelName)]
    return render_template('home.html', form=form, knownChannels=knownChannels)

@app.route("/results", methods=['GET', 'POST'])
def results():
    videos = Video.query.all()
    videos.sort(key=lambda v: v.publishedAt, reverse=True)
    return render_template('results.html', videos=videos, allChannels=True)

@app.route("/channel/<channelID>")
def channel(channelID):

    channel = channelPlaylist(channelID, maxResults=5, isUser=False)
    videoIDs = channel.videoIDs
    nVideosAdded = storeVideoInfoForChannel(channel)
    channelID = Video.query.filter_by(videoID=videoIDs[0]).first().channelID
    print(f"ADDED {nVideosAdded} VIDEO(S) TO DATABASE")

    videos = Video.query.filter_by(channelID=channelID).all()
    videos.sort(key=lambda v: v.publishedAt, reverse=True)
    print(videos[0].channelName)
    return render_template('results.html', videos=videos, allChannels=False)

@app.route("/channel/<channelID>/delete", methods=['GET','POST'])
def delete_channel(channelID):
    videos = Video.query.filter_by(channelID=channelID).all()
    if len(videos) == 0:
        abort(404)
    else:
        channelName = videos[0].channelName
        channelID = videos[0].channelID
        deleteThumbnail(channelID)
        for video in videos:
            deleteThumbnail(video.videoID)
            db.session.delete(video)
        db.session.commit()
        flash(f"Channel {channelName} has been deleted", 'success')
        return redirect(url_for('home'))

@app.route("/results/delete", methods=['GET','POST'])
def delete_results():
    videos = Video.query.all()
    if len(videos) == 0:
        abort(404)
    else:
        for video in videos:
            deleteThumbnail(video.channelID)
            deleteThumbnail(video.videoID)
            db.session.delete(video)
        db.session.commit()
        flash(f"All channels have been deleted", 'success')
        return redirect(url_for('home'))
