"""Social Stories application factory."""
import os
from flask import Flask
from flask_login import current_user

from app.extensions import db, login_manager, csrf
from config import config


def create_app(config_name=None):
    """Create and configure the Flask application.
    
    Args:
        config_name: Configuration environment name (development, testing, production)
        
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Ensure instance directory exists
    from pathlib import Path
    instance_dir = Path.cwd() / "instance"
    instance_dir.mkdir(exist_ok=True)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    app = Flask(__name__, 
                template_folder=str(project_root / 'templates'),
                static_folder=str(project_root / 'static'))
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Make current_user and csrf_token available in all templates
    @app.context_processor
    def inject_user():
        from flask_wtf.csrf import generate_csrf
        return dict(current_user=current_user, csrf_token=generate_csrf)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        from flask import render_template
        return render_template('errors/403.html'), 403


def register_blueprints(app):
    """Register application blueprints."""
    from app.main import main as main_bp
    from app.auth import auth as auth_bp
    from app.stories import stories as stories_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(stories_bp, url_prefix='/stories')