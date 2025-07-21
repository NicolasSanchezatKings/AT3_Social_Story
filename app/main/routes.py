from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.main import main
from app.main.forms import AccountForm, ContactForm
from app.extensions import db
from flask_mail import Message
import os


# Account editing page
@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm(obj=current_user)
    if form.validate_on_submit():
        # Update username and email
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.gemini_api_key = form.gemini_api_key.data
        current_user.serpapi_api_key = form.serpapi_api_key.data
        current_user.google_maps_api_key = form.google_maps_api_key.data

        # Handle profile picture upload
        profile_pic = form.profile_pic.data
        if profile_pic:
            filename = f"profile_{current_user.id}.png"
            filepath = os.path.join('static/img', filename)
            profile_pic.save(filepath)
            current_user.profile_pic_url = f"/static/img/{filename}"

        # Handle password change
        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('main.account'))
    return render_template('main/account.html', form=form, title='Edit Account')

# Privacy Policy page
@main.route('/privacy')
def privacy():
    return render_template('main/privacy.html', title='Privacy Policy')

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


@main.route('/help', methods=['GET', 'POST'])
def help():
    form = ContactForm()
    if form.validate_on_submit():
        # Send email (replace with your mail sending logic)
        # Example: using Flask-Mail
        try:
            msg = Message(
                subject=f"Support Request from {form.name.data}",
                sender=form.email.data,
                recipients=[current_app.config.get('SUPPORT_EMAIL', 'support@socialstories.com')],
                body=form.message.data
            )
            mail = current_app.extensions.get('mail')
            if mail:
                mail.send(msg)
            flash('Your message has been sent! We will get back to you soon.', 'success')
        except Exception as e:
            flash(f'Failed to send message: {e}', 'danger')
        return redirect(url_for('main.help'))
    return render_template('main/help.html', form=form)