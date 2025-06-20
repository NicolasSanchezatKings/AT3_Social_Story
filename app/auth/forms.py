"""Authentication forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form."""
    
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Length(min=2, max=20, message='Username must be between 2 and 20 characters.')
        ]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=6, message='Password must be at least 6 characters.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    """User login form."""
    
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestPasswordResetForm(FlaskForm):
    """Password reset request form."""
    
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        """Check if email exists in database."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    """Password reset form."""
    
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=6, message='Password must be at least 6 characters.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Reset Password')