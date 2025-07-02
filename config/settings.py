"""Application configuration module."""
import os
from pathlib import Path


class Config:
    """Base configuration class."""
    
    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # File uploads
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # Pagination
    STORIES_PER_PAGE = int(os.environ.get('STORIES_PER_PAGE', 10))
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Admin
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    
    @staticmethod
    def init_app(app):
        """Initialise application with configuration."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        f'sqlite:///{Path.cwd() / "instance" / "social_stories_dev.db"}'
    )
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Development-specific initialisation
        import logging
        from logging import StreamHandler
        
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        f'sqlite:///{Path.cwd() / "instance" / "social_stories.db"}'
    )
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific initialisation
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/social_stories.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Social Stories application startup')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}