from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from viewer.models import Video

class MySearchForm(FlaskForm):
    channelName = StringField('Enter channel/user name', validators=[DataRequired()])
    maxResults = IntegerField('Max Results', default=3)
    submit = SubmitField('Get Videos')
