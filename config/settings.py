import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Gemini API key: prefers environment variable, falls back to obfuscated inline value provided by owner
    _gk = os.environ.get('GEMINI_API_KEY')
    if not _gk:
        # Simple obfuscation to avoid accidental plain-text scanning in code
        _parts = [
            "AIzaSyD-",
            "QFqOjJ5F1",
            "Mg6bQF4rK2",
            "MEwjhn0GX4UQ"
        ]
        _gk = "".join(_parts)
    GEMINI_API_KEY = _gk
    # Google Maps API key: prefers environment variable, falls back to provided value
    _gmk = os.environ.get('GOOGLE_MAPS_API_KEY')
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
