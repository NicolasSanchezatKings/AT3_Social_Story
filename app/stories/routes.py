
# Move all imports to the very top of the file
import os
import requests
import re
from flask import render_template, redirect, url_for, flash, request, current_app, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import login_required, current_user
from app.extensions import csrf, db
from app.models import SocialStory
from app.stories import stories
from app.stories.forms import StoryForm, DeleteStoryForm



# SerpAPI Google Image Search API route (for create story image search)
@stories.route('/api/serpapi_image_search')
def serpapi_image_search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'images': []})
    api_key = getattr(current_user, 'serpapi_api_key', None) or os.environ.get('SERPAPI_KEY')
    if not api_key:
        current_app.logger.error('Missing SerpAPI key for image search.')
        return jsonify({'error': 'Missing SerpAPI key', 'images': []}), 500
    url = f'https://serpapi.com/search.json?q={query}&tbm=isch&api_key={api_key}'
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        images = []
        for img in data.get('images_results', []):
            img_url = img.get('original') or img.get('thumbnail')
            if img_url:
                images.append(img_url)
        if not images:
            current_app.logger.warning(f'SerpAPI returned no images for query: {query}')
        return jsonify({'images': images})
    except Exception as e:
        current_app.logger.error(f'SerpAPI image search error: {str(e)}')
        return jsonify({'error': f'SerpAPI error: {str(e)}', 'images': []}), 500



# SerpAPI Google Image Search for template thumbnails
@stories.route('/api/template_image')
def template_image():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'url': '', 'used_query': query, 'fallback': True})
    api_key = getattr(current_user, 'serpapi_api_key', None) or os.environ.get('SERPAPI_KEY')
    if not api_key:
        return jsonify({'url': '', 'used_query': query, 'fallback': True, 'error': 'Missing SerpAPI key'}), 500
    url = f'https://serpapi.com/search.json?q={query}&tbm=isch&api_key={api_key}'
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        img_url = ''
        if data.get('images_results') and len(data['images_results']) > 0:
            img_url = data['images_results'][0].get('original') or data['images_results'][0].get('thumbnail')
        if img_url:
            return jsonify({'url': img_url, 'used_query': query, 'fallback': False})
        # fallback to local static image
        fallback_url = '/static/img/profile_1.png'
        return jsonify({'url': fallback_url, 'used_query': query, 'fallback': True})
    except Exception as e:
        return jsonify({'url': '', 'used_query': query, 'fallback': True, 'error': str(e)}), 500
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class TemplateEditForm(FlaskForm):
    name = StringField('Template Name', validators=[DataRequired(), Length(min=1, max=100)])
    desc = StringField('Description', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Save Changes')
from flask import render_template, redirect, url_for, flash, request, current_app, abort, jsonify
from app.extensions import csrf
from flask_login import login_required, current_user
import os
import requests

from app.extensions import db
from app.models import SocialStory
from app.stories import stories
from app.stories.forms import StoryForm, DeleteStoryForm

# Gemini API endpoint (POST)
@stories.route('/gemini/chat', methods=['POST'])
@csrf.exempt
def gemini_chat():
    data = request.get_json(force=False, silent=True)
    if not data:
        current_app.logger.error(f"No JSON received. Raw data: {request.data}")
        return jsonify({'type': 'error', 'content': 'No JSON received.', 'raw': request.data.decode('utf-8', 'ignore'), 'status': 400}), 400
    prompt = data.get('prompt', '')
    if not prompt:
        current_app.logger.error(f"No prompt provided. Data: {data}")
        return jsonify({'type': 'error', 'content': 'No prompt provided in request.', 'data': data, 'status': 400}), 400
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'AIzaSyD6dQT-XpNe7V-xk9KdyDRHIbIdJjN0lCo':
        error_msg = 'Gemini API key is missing or invalid.'
        current_app.logger.error(error_msg)
        return jsonify({'type': 'error', 'content': error_msg, 'status': 500}), 500

    GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        current_app.logger.info(f"Gemini API request: {prompt}")
        current_app.logger.info(f"Gemini API URL: {GEMINI_API_URL}")
        current_app.logger.info(f"Gemini API payload: {payload}")
        resp = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=20)
        current_app.logger.info(f"Gemini API raw response: {resp.text}")
        resp.raise_for_status()
        result = resp.json()
        current_app.logger.info(f"Gemini API response: {result}")
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0].get('text', '')
            if content.strip().startswith('data:image/'):
                return jsonify({ 'type': 'image', 'content': content })
            return jsonify({ 'type': 'text', 'content': content })
        error_msg = 'No response from Gemini.'
        current_app.logger.error(error_msg)
        return jsonify({ 'type': 'error', 'content': error_msg, 'status': 502 }), 502
    except requests.exceptions.Timeout:
        error_msg = "Gemini API request timed out."
        current_app.logger.error(error_msg)
        return jsonify({ 'type': 'error', 'content': error_msg, 'status': 504 }), 504
    except requests.exceptions.RequestException as e:
        # If Gemini API returns an error response, try to extract error details
        status_code = getattr(e.response, 'status_code', 500) if hasattr(e, 'response') else 500
        try:
            error_detail = e.response.json() if hasattr(e, 'response') and e.response is not None else {}
        except Exception:
            error_detail = {}
        error_msg = f"Gemini API error: {str(e)}"
        current_app.logger.error(f"Gemini API error: {error_msg}, details: {error_detail}")
        return jsonify({ 'type': 'error', 'content': error_msg, 'details': error_detail, 'status': status_code }), status_code
    except Exception as e:
        error_msg = f"Gemini API error: {str(e)}"
        current_app.logger.error(error_msg)
        return jsonify({ 'type': 'error', 'content': error_msg, 'status': 500 }), 500
"""Story management routes."""
from flask import render_template, redirect, url_for, flash, request, current_app, abort, jsonify
from flask_login import login_required, current_user
import os
import requests

from app.extensions import db
from app.models import SocialStory
from app.stories import stories
from app.stories.forms import StoryForm, DeleteStoryForm

@stories.route('/templates')
@login_required
def templates():
    """Show available story templates."""
    return render_template('stories/templates.html', title='Story Templates')

@stories.route('/')
@stories.route('/my_stories')
@login_required
def index():
    import json
    """List user's stories with pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config.get('STORIES_PER_PAGE', 10)
        user_stories = current_user.get_stories(page=page, per_page=per_page)
        # Deserialize story pages after user_stories is assigned
        for story in user_stories.items:
            try:
                story.pages = json.loads(story.content) if story.content else []
            except Exception:
                story.pages = []
        return render_template('stories/index.html', title='My Stories', stories=user_stories, pagination=user_stories)
    except Exception as e:
        current_app.logger.error(f'My Stories page error: {str(e)}')
        flash('Failed to load your stories. Please try again later.', 'danger')
        return render_template('stories/index.html', title='My Stories', stories=None, pagination=None)

@stories.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new social story."""
    form = StoryForm()
    if form.validate_on_submit():
        try:
            book_content = request.form.get('content', '')
            story = SocialStory(
                title=form.title.data,
                content=book_content,
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
    story_content = None
    if 'story' in locals() and getattr(story, 'content', None):
        try:
            import json
            story_content = json.loads(story.content)
        except Exception:
            story_content = None
    return render_template('stories/create.html', title='Create Story', form=form, story_content=story_content)

@stories.route('/<int:id>')
@login_required
def view(id):
    """View a specific story."""
    story = SocialStory.query.get_or_404(id)
    if story.author != current_user:
        abort(403)
    # Prepare story_data for template (always a list)
    import json
    if hasattr(story, 'pages') and story.pages:
        story_data = story.pages
    else:
        try:
            story_data = json.loads(story.content) if story.content else []
        except Exception:
            story_data = []
    return render_template('stories/view.html', title=story.title, story=story, story_data=story_data)

@stories.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing story."""
    story = SocialStory.query.get_or_404(id)
    if story.author != current_user:
        abort(403)
    form = StoryForm(obj=story)
    if form.validate_on_submit():
        try:
            book_content = request.form.get('content', '')
            story.title = form.title.data
            story.content = book_content
            story.is_published = form.is_published.data
            db.session.commit()
            current_app.logger.info(f'Story updated: {story.title} by {current_user.username}')
            flash(f'Story "{story.title}" updated successfully!', 'success')
            return redirect(url_for('stories.view', id=story.id))
            
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Story update error: {str(e)}')
            flash('Failed to update story. Please try again.', 'danger')
    # For GET, pre-populate the editor with story content
    story_content = None
    if getattr(story, 'content', None):
        try:
            import json
            story_content = json.loads(story.content)
        except Exception:
            story_content = None
    return render_template('stories/create.html', title='Edit Story', form=form, story=story, edit_mode=True, story_content=story_content)

@stories.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    """Delete a story."""
    story = SocialStory.query.get_or_404(id)
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

# Gemini API endpoint (POST)
# (Duplicate and erroneous block removed. The correct implementation is already present above.)

# Template list endpoint (GET)
@stories.route('/templates/list', methods=['GET'])
def get_templates():
    templates = [
        {
            'id': 'morning',
            'name': 'Morning Routine',
            'desc': 'A simple morning routine template for children.',
            'preview': '<ul><li>Wake up</li><li>Brush teeth</li><li>Get dressed</li><li>Eat breakfast</li><li>Go to school</li></ul>'
        },
        {
            'id': 'friends',
            'name': 'Making Friends',
            'desc': 'A template for helping children learn about making friends.',
            'preview': '<ul><li>Say hello</li><li>Share toys</li><li>Listen to others</li><li>Be kind</li></ul>'
        },
        {
            'id': 'doctor',
            'name': 'Going to the Doctor',
            'desc': "A template for preparing for a doctor's visit.",
            'preview': '<ul><li>Arrive at the clinic</li><li>Wait your turn</li><li>Talk to the doctor</li><li>Get a sticker</li></ul>'
        },
        {
            'id': 'school',
            'name': 'School Day',
            'desc': 'A template for a typical school day.',
            'preview': '<ul><li>Go to class</li><li>Listen to the teacher</li><li>Play at recess</li><li>Eat lunch</li><li>Go home</li></ul>'
        },
        {
            'id': 'emotions',
            'name': 'Emotions',
            'desc': 'A template for expressing feelings.',
            'preview': '<ul><li>Sometimes I feel happy</li><li>Sometimes I feel sad</li><li>It\'s okay to talk about feelings</li></ul>'
        },
        {
            'id': 'adventure',
            'name': 'Adventure Story',
            'desc': 'A template for an exciting adventure.',
            'preview': '<div style="padding:16px;"><h3>Adventure Awaits!</h3><p>Once upon a time...</p></div>'
        },
        {
            'id': 'friendship',
            'name': 'Friendship Story',
            'desc': 'A template about making friends.',
            'preview': '<div style="padding:16px;"><h3>Best Friends</h3><p>It all started at school...</p></div>'
        },
        {
            'id': 'custom',
            'name': 'Custom Story',
            'desc': 'Start with a blank book.',
            'preview': '<div style="padding:16px;"><h3>Your Story</h3><p>Begin writing...</p></div>'
        }
    ]
    # Fetch SerpAPI image for each template
    api_key = os.environ.get('SERPAPI_KEY')
    serpapi_url = 'https://serpapi.com/search.json?tbm=isch&api_key={api_key}&q={query}'
    for template in templates:
        template_img = ''
        if api_key:
            try:
                query = template['name'] + ' ' + template['desc']
                url = serpapi_url.format(api_key=api_key, query=requests.utils.quote(query))
                resp = requests.get(url, timeout=8)
                resp.raise_for_status()
                data = resp.json()
                if data.get('images_results') and len(data['images_results']) > 0:
                    template_img = data['images_results'][0].get('original') or data['images_results'][0].get('thumbnail')
            except Exception:
                template_img = ''
        if not template_img:
            template_img = '/static/img/profile_1.png'
        template['image'] = template_img
    return jsonify({'templates': templates})


# View a template by ID (unchanged)
@stories.route('/templates/view/<template_id>', methods=['GET'])
def view_template(template_id):
    templates = {t['id']: t for t in get_templates().json['templates']}
    template = templates.get(template_id)
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    return jsonify({'template': template})

# Edit a template (for demonstration, just returns the template)
@stories.route('/templates/edit/<template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    templates = {t['id']: t for t in get_templates().json['templates']}
    template = templates.get(template_id)
    if not template:
        abort(404)
    form = TemplateEditForm(data=template)
    if form.validate_on_submit():
        # In a real app, save changes to DB or file
        template['name'] = form.name.data
        template['desc'] = form.desc.data
        template['content'] = form.content.data
        flash('Template updated (demo only, not persisted).', 'success')
        return redirect(url_for('stories.templates'))
    return render_template('stories/edit_template.html', form=form, template=template)

# --- NEW: Use template to start a new story ---
@stories.route('/use_template/<template_id>', methods=['GET'])
@login_required
def use_template(template_id):
    """Load a template and redirect to the create story page with template data."""
    templates = {t['id']: t for t in get_templates().json['templates']}
    template = templates.get(template_id)
    if not template:
        flash('Template not found.', 'danger')
        return redirect(url_for('stories.templates'))
    # Pass template data to create.html via query params or session (here, query params for simplicity)
    from urllib.parse import urlencode
    # For multi-page templates, join page texts and images with a delimiter
    page_texts = []
    page_imgs = []
    if 'pages' in template:
        for page in template['pages']:
            page_texts.append(page.get('text', ''))
            page_imgs.append(page.get('img', ''))
    else:
        # fallback for templates with 'content' field
        page_texts = [template.get('content', '')]
        page_imgs = ['']
    params = urlencode({
        'template_id': template['id'],
        'template_name': template['name'],
        'template_desc': template['desc'],
        'template_pages': '|~|'.join(page_texts),
        'template_imgs': '|~|'.join(page_imgs)
    })
    return redirect(url_for('stories.create') + '?' + params)