#!/usr/bin/env python3
"""
Setup script for the Educational Video Generator Backend
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_file = Path(".env")
    example_file = Path("env.example")
    
    if not env_file.exists() and example_file.exists():
        shutil.copy(example_file, env_file)
        print("✅ Created .env file from example")
        print("⚠️  Please edit .env file with your API keys")
        return False
    elif not env_file.exists():
        print("❌ No .env file found. Please create one with your API keys")
        return False
    else:
        print("✅ .env file exists")
        return True

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["uploads", "outputs", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def check_api_keys():
    """Check if API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    tts_key = os.getenv("TTS_API_KEY")
    
    if gemini_key and gemini_key != "your_google_gemini_api_key_here":
        print("✅ Gemini API key configured")
    else:
        print("⚠️  Gemini API key not configured (will use mock responses)")
    
    if tts_key and tts_key != "your_elevenlabs_api_key_here":
        print("✅ ElevenLabs API key configured")
    else:
        print("⚠️  ElevenLabs API key not configured (TTS will be disabled)")

def main():
    """Main setup function"""
    print("🚀 Setting up Educational Video Generator Backend...\n")
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Create .env file
    env_created = create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check API keys
    check_api_keys()
    
    print("\n🎉 Setup completed!")
    
    if not env_created:
        print("\n📝 Next steps:")
        print("1. Edit the .env file with your API keys")
        print("2. Run: python start.py")
    else:
        print("\n📝 To start the server, run: python start.py")
    
    print("\n📚 API documentation will be available at: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 