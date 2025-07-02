"""Authentication routes."""
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required

from app.extensions import db
from app.models import User
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data.lower()
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            current_app.logger.info(f'New user registered: {user.username}')
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {str(e)}')
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            current_app.logger.info(f'User logged in: {user.username}')
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
    """User logout endpoint."""
    username = current_user.username
    logout_user()
    current_app.logger.info(f'User logged out: {username}')
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))