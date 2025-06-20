"""Main application routes."""
from flask import render_template, current_app
from flask_login import current_user

from app.main import main
from app.models import SocialStory


@main.route('/')
def index():
    """Home page route."""
    recent_stories = []
    if current_user.is_authenticated:
        recent_stories = current_user.stories.order_by(
            SocialStory.created_at.desc()
        ).limit(5).all()
    
    return render_template(
        'main/index.html',
        title='Home',
        recent_stories=recent_stories
    )


@main.route('/about')
def about():
    """About page route."""
    return render_template('main/about.html', title='About')


@main.route('/help')
def help():
    """Help page route."""
    return render_template('main/help.html', title='Help')