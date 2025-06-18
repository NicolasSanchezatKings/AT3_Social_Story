from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask import current_app
from app.models import SocialStory
from app.stories import stories
from app.stories.forms import StoryForm
from app.models import SocialStory

@stories.route('/stories')
@login_required
def list_stories():
    user_stories = SocialStory.query.filter_by(author=current_user).all()
    return render_template('stories/list.html', stories=user_stories)

@stories.route('/stories/create', methods=['GET', 'POST'])
@login_required
def create_story():
    from app.extensions import db
    form = StoryForm()
    if form.validate_on_submit():
        story = SocialStory(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(story)
        db.session.commit()
        flash('Story created successfully!', 'success')
        return redirect(url_for('stories.list_stories'))
    return render_template('stories/create.html', form=form)

@stories.route('/stories/<int:story_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_story(story_id):
    from app.extensions import db
    story = SocialStory.query.get_or_404(story_id)
    if story.author != current_user:
        flash("You don't have permission to edit this story.", 'danger')
        return redirect(url_for('stories.list_stories'))

    form = StoryForm(obj=story)
    if form.validate_on_submit():
        story.title = form.title.data
        story.content = form.content.data
        db.session.commit()
        flash('Story updated!', 'success')
        return redirect(url_for('stories.list_stories'))
    return render_template('stories/edit.html', form=form)

@stories.route('/stories/<int:story_id>/delete', methods=['POST'])
@login_required
def delete_story(story_id):
    from app.extensions import db
    story = SocialStory.query.get_or_404(story_id)
    if story.author != current_user:
        flash("You don't have permission to delete this story.", 'danger')
        return redirect(url_for('stories.list_stories'))
    
    db.session.delete(story)
    db.session.commit()
    flash('Story deleted.', 'info')
    return redirect(url_for('stories.list_stories'))
