from flask import Flask
from flask_login import current_user
from app.extensions import db, login_manager

# Blueprints
from app.auth import auth
from app.main import main
from app.stories import stories

login_manager.login_view = 'auth.login'

def create_app():
    # ✅ Create the app with custom template path
    app = Flask(__name__, template_folder='/Users/nicolassanchez/Software Engineering Project/social_story_app/frontend/templates')

    # ✅ Configurations
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # ✅ Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # ✅ Make current_user available in templates
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # ✅ Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(stories)

    return app
