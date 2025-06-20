#!/usr/bin/env python3
"""
Social Stories Application Entry Point

This module serves as the main entry point for the Social Stories web application.
It creates the Flask application instance and runs the development server.
"""

import os
from app import create_app

# Create the Flask application
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Print available routes for debugging
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint:30} {rule}")
    
    # Run the application
    app.run(
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'on']
    )