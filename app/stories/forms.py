"""Story forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class StoryForm(FlaskForm):
    """Social story creation and editing form."""
    
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=1, max=150, message='Title must be between 1 and 150 characters.')
        ]
    )
    content = TextAreaField(
        'Content',
        validators=[
            DataRequired(),
            Length(min=10, message='Content must be at least 10 characters.')
        ]
    )
    is_published = BooleanField('Publish this story')
    submit = SubmitField('Save Story')


class DeleteStoryForm(FlaskForm):
    """Story deletion confirmation form."""
    
    submit = SubmitField('Delete Story')