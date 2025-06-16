import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    TTS_API_KEY: str = os.getenv("TTS_API_KEY", "")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Frontend URL for CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Directories
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./outputs")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "./templates")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./videos.db")
    
    # Video Generation Settings
    MAX_VIDEO_DURATION: int = int(os.getenv("MAX_VIDEO_DURATION", "60"))
    DEFAULT_VOICE_ID: str = os.getenv("DEFAULT_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
    
    # Ensure directories exist
    def __post_init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.TEMPLATES_DIR, exist_ok=True)

settings = Settings()

# Create directories on import
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
