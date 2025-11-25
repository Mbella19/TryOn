import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Resolve important paths up front
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Always load the .env that sits next to this config, even when the app
# is started from a different working directory (e.g., project root).
load_dotenv(BASE_DIR / ".env")


def _build_db_uri() -> str:
    """Return a fully-qualified SQLite URI, normalizing relative paths."""
    env_uri = os.getenv("DATABASE_URL")
    default_path = BASE_DIR / "instance" / "tryon.db"

    if env_uri and env_uri.startswith("sqlite:///"):
        db_path = env_uri.replace("sqlite:///", "", 1)
        db_path = Path(db_path)
        if not db_path.is_absolute():
            db_path = BASE_DIR / db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"

    default_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{default_path}"

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    @staticmethod
    def init_app(app):
        """Validate required configuration"""
        pass
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(BASE_DIR), os.getenv('UPLOAD_FOLDER', 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Google Gemini Configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    # Allow defaults only in development
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-key-change-in-prod')

class ProductionConfig(Config):
    """Production configuration - requires all secrets to be set"""
    DEBUG = False
    FLASK_ENV = 'production'

    @staticmethod
    def init_app(app):
        """Validate required secrets are set in production"""
        required = ['SECRET_KEY', 'JWT_SECRET_KEY', 'GOOGLE_API_KEY']
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise ValueError(f"Missing required environment variables for production: {', '.join(missing)}")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
