from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gemini_api_key = StringField('Gemini API Key', validators=[Optional(), Length(max=128)])
    serpapi_api_key = StringField('SerpAPI Key', validators=[Optional(), Length(max=128)])
    google_maps_api_key = StringField('Google Maps API Key', validators=[Optional(), Length(max=128)])
    profile_pic = FileField('Profile Picture', validators=[Optional()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Save Changes')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Your Email', validators=[DataRequired(), Email(), Length(max=120)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Send Message')
