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
    videoUrl = db.Column(db.String(50), unique=False, nullable=False)
    #thumbnails = db.Column(db.String(20), nullable=False, default='default.jpg')
    description = db.Column(db.String(5000))

    def __repr__(self):
        return f"Video('{self.title}', '{self.channelName}')"
