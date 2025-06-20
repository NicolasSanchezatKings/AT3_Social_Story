#!/usr/bin/env python3
"""
Setup script for Social Stories Application
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description=""):
    """Run a command and handle errors."""
    print(f"Running: {description or command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is adequate."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def create_directories():
    """Create necessary directories."""
    directories = ['instance', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def setup_environment():
    """Set up environment file if it doesn't exist."""
    env_file = Path('.env')
    if not env_file.exists():
        env_example = Path('.env.example')
        if env_example.exists():
            # Copy .env.example to .env
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✓ Created .env file from .env.example")
            print("⚠️  Please edit .env and set your SECRET_KEY before running the application")
        else:
            # Create minimal .env file
            with open(env_file, 'w') as f:
                f.write("SECRET_KEY=change-this-to-a-random-secret-key\n")
                f.write("FLASK_ENV=development\n")
                f.write("FLASK_DEBUG=True\n")
            print("✓ Created basic .env file")
            print("⚠️  Please edit .env and change the SECRET_KEY before running the application")
    else:
        print("✓ .env file already exists")


def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    
    # Try to install requirements
    if not run_command("pip install -r requirements.txt", "Installing core dependencies"):
        print("Failed to install dependencies. Please check your pip installation.")
        return False
    
    print("✓ Dependencies installed successfully")
    return True


def main():
    """Main setup function."""
    print("🚀 Setting up Social Stories Application")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create necessary directories
    create_directories()
    
    # Set up environment
    setup_environment()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit the .env file and set a secure SECRET_KEY")
    print("2. Run the application with: python3 run.py")
    print("3. Open your browser to http://127.0.0.1:5000")
    print("\nFor help, see README.md or visit /help in the application")


if __name__ == "__main__":
    main()