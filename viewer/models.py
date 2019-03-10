from datetime import datetime
from viewer import db

def utc_to_local(utc_dt_string):
    utc_dt = datetime.strptime(utc_dt_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return datetime.strftime(local_dt, "%Y-%m-%d %I:%M %p")

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    channelName = db.Column(db.String(20), unique=False, nullable=False)
    publishedAt = db.Column(db.String(20), unique=False, nullable=False)
    videoID = db.Column(db.String(20), unique=False, nullable=False)
    videoUrl = db.Column(db.String(50), unique=False, nullable=False)
    image = db.Column(db.String(60), unique=False, nullable=True, default="")
    description = db.Column(db.String(1000))
    def __repr__(self):
        return f"Video('{self.title}', {self.videoID}, '{self.channelName}, {self.image}')"
