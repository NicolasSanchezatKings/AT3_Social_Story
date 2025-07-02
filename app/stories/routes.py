"""Story management routes."""
from flask import render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.models import SocialStory
from app.stories import stories
from app.stories.forms import StoryForm, DeleteStoryForm


@stories.route('/')
@login_required
def index():
    """List user's stories with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('STORIES_PER_PAGE', 10)
    
    user_stories = current_user.get_stories(page=page, per_page=per_page)
    
    return render_template(
        'stories/index.html',
        title='My Stories',
        stories=user_stories,
        pagination=user_stories
    )


@stories.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new social story."""
    form = StoryForm()
    
    if form.validate_on_submit():
        try:
            story = SocialStory(
                title=form.title.data,
                content=form.content.data,
                is_published=form.is_published.data,
                author=current_user
            )
            
            db.session.add(story)
            db.session.commit()
            
            current_app.logger.info(f'Story created: {story.title} by {current_user.username}')
            flash(f'Story "{story.title}" created successfully!', 'success')
            return redirect(url_for('stories.view', id=story.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Story creation error: {str(e)}')
            flash('Failed to create story. Please try again.', 'danger')
    
    return render_template('stories/create.html', title='Create Story', form=form)


@stories.route('/<int:id>')
@login_required
def view(id):
    """View a specific story."""
    story = SocialStory.query.get_or_404(id)
    
    # Check if user owns the story
    if story.author != current_user:
        abort(403)
    
    return render_template('stories/view.html', title=story.title, story=story)


@stories.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing story."""
    story = SocialStory.query.get_or_404(id)
    
    # Check if user owns the story
    if story.author != current_user:
        abort(403)
    
    form = StoryForm(obj=story)
    
    if form.validate_on_submit():
        try:
            story.title = form.title.data
            story.content = form.content.data
            story.is_published = form.is_published.data
            
            db.session.commit()
            
            current_app.logger.info(f'Story updated: {story.title} by {current_user.username}')
            flash(f'Story "{story.title}" updated successfully!', 'success')
            return redirect(url_for('stories.view', id=story.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Story update error: {str(e)}')
            flash('Failed to update story. Please try again.', 'danger')
    
    return render_template('stories/edit.html', title='Edit Story', form=form, story=story)


@stories.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    """Delete a story."""
    story = SocialStory.query.get_or_404(id)
    
    # Check if user owns the story
    if story.author != current_user:
        abort(403)
    
    form = DeleteStoryForm()
    
    if form.validate_on_submit():
        try:
            story_title = story.title
            db.session.delete(story)
            db.session.commit()
            
            current_app.logger.info(f'Story deleted: {story_title} by {current_user.username}')
            flash(f'Story "{story_title}" deleted successfully.', 'info')
            return redirect(url_for('stories.index'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Story deletion error: {str(e)}')
            flash('Failed to delete story. Please try again.', 'danger')
    
    return render_template('stories/delete.html', title='Delete Story', form=form, story=story)