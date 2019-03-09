from datetime import datetime
from viewer import db

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
