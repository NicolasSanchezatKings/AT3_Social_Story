# Social Stories Web Application

A comprehensive web application for creating, managing, and sharing social stories to help individuals understand and navigate social situations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

Social Stories are short descriptions of social situations that help individuals, particularly those with autism spectrum disorders, understand and respond appropriately to various social contexts. This web application provides a user-friendly platform for creating, editing, and managing personalised social stories.

### What are Social Stories?

Social stories are evidence-based tools that:
- Help individuals understand social situations
- Provide clear expectations for behaviour
- Reduce anxiety in social contexts
- Promote independence and confidence
- Support learning and development

## ✨ Features

### Core Features
- **User Authentication**: Secure registration and login system
- **Story Management**: Create, read, update, and delete social stories
- **Rich Text Editor**: Intuitive interface for writing stories
- **Auto-Save**: Automatic draft saving to prevent data loss
- **Story Preview**: Preview stories before saving
- **Publication Status**: Mark stories as drafts or published
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### User Experience
- **Clean Interface**: Modern, accessible design using Bootstrap 5
- **Search & Filter**: Find stories quickly
- **Pagination**: Efficient navigation through large story collections
- **Flash Messages**: Clear feedback for user actions
- **Keyboard Navigation**: Full accessibility support
- **Error Handling**: Graceful error management and user feedback

### Security Features
- **Password Hashing**: Secure password storage using Werkzeug
- **CSRF Protection**: Cross-site request forgery prevention
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: Protected database queries
- **Session Management**: Secure user session handling

## 📁 Project Structure

```
AT3_Social_Story_Nick_S/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Flask extensions
│   ├── models.py                # Database models
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── forms.py             # Authentication forms
│   │   └── routes.py            # Authentication routes
│   ├── main/                    # Main application blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Main routes (home, about, etc.)
│   └── stories/                 # Stories management blueprint
│       ├── __init__.py
│       ├── forms.py             # Story forms
│       └── routes.py            # Story management routes
├── config/                      # Configuration modules
│   ├── __init__.py
│   └── settings.py              # Application settings
├── static/                      # Static assets
│   ├── css/
│   │   └── main.css             # Custom styles
│   ├── js/
│   │   └── main.js              # JavaScript functionality
│   └── img/
│       └── favicon.ico          # Site favicon
├── templates/                   # Jinja2 templates
│   ├── layout/
│   │   └── base.html            # Base template
│   ├── main/
│   │   ├── index.html           # Home page
│   │   ├── about.html           # About page
│   │   └── help.html            # Help page
│   ├── auth/
│   │   ├── login.html           # Login page
│   │   └── register.html        # Registration page
│   ├── stories/
│   │   ├── index.html           # Stories list
│   │   ├── create.html          # Create story
│   │   ├── edit.html            # Edit story
│   │   ├── view.html            # View story
│   │   └── delete.html          # Delete confirmation
│   └── errors/                  # Error pages
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
├── instance/                    # Instance-specific files
│   └── social_stories_dev.db    # SQLite database (created at runtime)
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Project configuration
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Setup script
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AT3_Social_Story_Nick_S.git
   cd AT3_Social_Story_Nick_S
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Production dependencies
   pip install -r requirements.txt
   
   # For development (includes testing and linting tools)
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # At minimum, set a secure SECRET_KEY
   ```

5. **Initialize the database**
   ```bash
   python run.py
   # The database will be created automatically on first run
   ```

6. **Access the application**
   - Open your browser and go to `http://127.0.0.1:5000`
   - Register a new account to get started

## ⚙️ Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

### Required Configuration
```env
SECRET_KEY=your-secret-key-here-make-it-long-and-random
```

### Optional Configuration
```env
# Flask settings
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///instance/social_stories.db

# Application settings
STORIES_PER_PAGE=10
MAX_CONTENT_LENGTH=16777216

# Email (for future features)
MAIL_SERVER=localhost
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=
```

### Configuration Environments

The application supports multiple environments:

- **Development** (`development`): Debug enabled, verbose logging
- **Testing** (`testing`): In-memory database, CSRF disabled
- **Production** (`production`): Optimised for performance and security

Set the environment using:
```bash
export FLASK_ENV=production  # or development, testing
```

## 💻 Usage

### For End Users

1. **Registration**: Create a new account with username, email, and password
2. **Login**: Access your account with email and password
3. **Create Stories**: Use the intuitive editor to write social stories
4. **Manage Stories**: View, edit, or delete your stories from the dashboard
5. **Preview**: Preview stories before saving
6. **Publish**: Mark stories as published when ready for use

### Story Writing Tips

- **Use first person**: Write from the perspective of the person who will read the story
- **Be specific**: Describe exactly what will happen and when
- **Stay positive**: Focus on what to do rather than what not to do
- **Keep it simple**: Use clear, age-appropriate language
- **Include context**: Describe the setting and circumstances

### Example Story Structure
```
Title: Going to the Grocery Store

When I go to the grocery store with my family, I will:

1. Get a shopping cart or basket at the entrance
2. Walk slowly and stay close to my family
3. Use my quiet voice when talking
4. Keep my hands in my pockets unless I need to help
5. Wait patiently in line at the checkout
6. Say "thank you" to the cashier

Following these steps helps me have a successful shopping trip.
This makes me feel proud and confident.
```

## 🛠️ Development

### Development Setup

1. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run the development server**
   ```bash
   python run.py
   ```

### Code Quality

The application follows Python best practices and PEP 8 style guidelines.

### Database Management

The application uses SQLAlchemy with SQLite by default. The database is created automatically when you first run the application.

#### Database Schema

- **Users**: Store user authentication information
- **Social Stories**: Store story content and metadata

#### Manual Database Operations

```python
# In Python shell or script
from app import create_app, db
from app.models import User, SocialStory

app = create_app()
with app.app_context():
    # Create all tables
    db.create_all()
    
    # Create a test user
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
```

## 🧪 Testing

The application includes basic testing configuration. To add tests, create a `tests/` directory and use pytest:

```bash
# Install testing dependencies
pip install -r requirements-dev.txt

# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

Basic test structure is configured in `pyproject.toml` for future expansion.

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   ```

2. **Install Production Server**
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
   ```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

### Environment Variables for Production

Ensure these are set in production:
- `SECRET_KEY`: Strong, random secret key
- `DATABASE_URL`: Production database connection string
- `FLASK_ENV=production`
- Any email or external service credentials

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   pytest
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your feature"
   ```
6. **Push and create a pull request**

### Code Standards

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages
- Keep functions small and focused

### Reporting Issues

When reporting bugs, please include:
- Steps to reproduce the issue
- Expected vs actual behavior
- Browser and version (if applicable)
- Error messages or screenshots

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library
- Social Stories concept by Carol Gray

## 📞 Support

If you encounter any issues or have questions:

1. Check the in-application help at `/help`
2. Review this README file
3. Create a new issue if needed
4. Contact the development team

---

Built with ❤️ for inclusive education and social learning.