import os

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use environment variables directly

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Gemini API key: prefers environment variable or .env file, falls back to provided value
    # Get your API key from: https://makersuite.google.com/app/apikey
    # Set it as: export GEMINI_API_KEY="your-api-key-here" or add to .env file
    _gk = os.environ.get('GEMINI_API_KEY')
    GEMINI_API_KEY = _gk
    # Google Maps API key: prefers environment variable, falls back to provided value
    _gmk = os.environ.get('GOOGLE_MAPS_API_KEY')
    print(f"DEBUG: GEMINI_API_KEY loaded: {GEMINI_API_KEY[:10]}..." if GEMINI_API_KEY else "DEBUG: GEMINI_API_KEY is None")
    if not _gmk:
        # API key provided by user
        _gmk = "AIzaSyCbCnDoaCIG858aOJKmoXhmapxwnhwOzlA"
    GOOGLE_MAPS_API_KEY = _gmk

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DB_FILE = os.path.join(BASE_DIR, 'users.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE}'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Add production database URI here
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}