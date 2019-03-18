import os
import sys
sys.path.append('..')

from flask import render_template, url_for, flash, redirect, request, session, abort
from viewer import app, db
from viewer.forms import SearchForm #RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from viewer.models import Video #User, Post
#from flask_login import login_user, current_user, logout_user, login_required
from viewer.serverUtils import utc_to_local, downloadThumbnail, downloadChannelImage, storeVideoInfoForChannel, deleteThumbnail, downloadVideo
from youtubeUtils import channelPlaylist


#global videos
#videos = []




@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    #videos = Video.query.all()
    form = SearchForm()
    session['maxResults'] = form.maxResults.data
    if form.validate_on_submit():
        channel = channelPlaylist(form.channelName.data, maxResults=form.maxResults.data)
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
    print("MAX RESULTS: ", session.get('maxResults', None))
    channel = channelPlaylist(channelID, maxResults=session.get('maxResults', None))
    videoIDs = channel.videoIDs
    nVideosAdded = storeVideoInfoForChannel(channel)
    channelID = Video.query.filter_by(videoID=videoIDs[0]).first().channelID
    print(f"ADDED {nVideosAdded} VIDEO(S) TO DATABASE")

    videos = Video.query.filter_by(channelID=channelID).all()
    videos.sort(key=lambda v: v.publishedAt, reverse=True)

    return render_template('results.html', videos=videos, allChannels=False)

@app.route("/channel/<channelID>/<videoID>", methods=['GET','POST'])
def watch_video_mpv(channelID, videoID):
    video = Video.query.filter_by(videoID=videoID).first()
    mpv_success = video.play_mpv()
    if mpv_success:
        flash(f"Playing {video.title} from channel {video.channelName} in terminal with MPV", 'info')
    else:
        flash(f"Failed to play {video.title} from channel {video.channelName} with MPV", 'info')
    return redirect(url_for('channel', channelID=channelID))

@app.route("/channel/<channelID>/<videoID>/kill", methods=['GET','POST'])
def kill_video_mpv(channelID, videoID):
    video = Video.query.filter_by(videoID=videoID).first()
    print(video.status())
    if video.status() == True:
        video.kill_mpv()
    return redirect(url_for('channel', channelID=channelID))

@app.route("/channel/<channelID>/<videoID>/download", methods=['GET','POST'])
def download_video(channelID, videoID):
    video = Video.query.filter_by(videoID=videoID).first()
    mp4file = downloadVideo(video.videoUrl, video.title)
    video.mp4file = mp4file
    db.session.commit()
    return redirect(url_for('channel', channelID=channelID))

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
