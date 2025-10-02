#!/usr/bin/env python3
"""
Setup script for Podgaku Podcast RSS Generator
Helps new users get started quickly
"""
import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🎙️" + "=" * 50)
    print("   Podgaku Podcast RSS Generator Setup")
    print("   Welcome! Let's get your podcast ready")
    print("=" * 52)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("💡 Try: pip install -r requirements.txt")
        return False

def setup_env_file():
    """Help user set up environment file"""
    print("\n🔧 Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    # Copy example file
    with open(env_example, 'r') as src, open(env_file, 'w') as dst:
        dst.write(src.read())
    
    print("✅ Created .env file from template")
    print("⚠️  IMPORTANT: Edit .env file with your actual credentials")
    print("   - PODCAST_DOMAIN: Your domain name")
    print("   - FTP_HOST: Your server hostname")
    print("   - FTP_USERNAME: Your SFTP username")
    print("   - FTP_PASSWORD: Your SFTP password")
    print("   - FTP_EPISODES_DIR: Server path for episodes")
    print("   - FTP_RSS_PATH: Server path for RSS file")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['uploads', 'episodes', 'static/img']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    return True

def setup_podcast_config():
    """Guide user through podcast configuration"""
    print("\n📝 Podcast configuration...")
    
    config_file = Path("podcast_config.py")
    if not config_file.exists():
        print("❌ podcast_config.py not found")
        return False
    
    print("✅ Found podcast_config.py")
    print("⚠️  IMPORTANT: Edit podcast_config.py with your podcast information")
    print("   - title: Your podcast name")
    print("   - description: Podcast description")
    print("   - author: Your name")
    print("   - email: Contact email")
    print("   - website: Your website")
    print("   - image_url: Podcast cover image URL")
    
    return True

def show_next_steps():
    """Show user what to do next"""
    print("\n🚀 Setup complete! Next steps:")
    print()
    print("1. 📝 Edit configuration files:")
    print("   - .env (server credentials)")
    print("   - podcast_config.py (podcast info)")
    print()
    print("2. 🎵 Add your first episode:")
    print("   python start_web.py")
    print("   # Then visit http://localhost:8080/admin")
    print()
    print("3. 📡 Deploy to your server:")
    print("   python deploy_to_ftp.py")
    print()
    print("4. 🌐 Deploy web frontend:")
    print("   python upload_web.py")
    print()
    print("📚 For detailed instructions, see README.md")
    print("🆘 For help, visit: https://github.com/yourusername/podcastXMLgen")

def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Setup configuration
    if not setup_env_file():
        return 1
    
    # Create directories
    if not create_directories():
        return 1
    
    # Setup podcast config
    if not setup_podcast_config():
        return 1
    
    # Show next steps
    show_next_steps()
    
    print("\n🎉 Setup completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
