from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask import session
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from viewer.models import Video

class SearchForm(FlaskForm):
    channelName = StringField('Channel name or ID:', validators=[DataRequired()])
    maxResults = IntegerField('# Videos: ', default=3)
    isUser = BooleanField('username', default=True)
    submit = SubmitField('Add')
