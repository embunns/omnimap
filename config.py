import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # PostgreSQL Configuration
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'omnimap_db')
    
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    
    # Fallback ke SQLite jika PostgreSQL gagal
    SQLALCHEMY_DATABASE_URI_FALLBACK = 'sqlite:///omnimap.db'
    
    # Auto-detect which database is being used
    @staticmethod
    def get_current_db_type(app):
        """Detect if using PostgreSQL or SQLite"""
        uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'postgresql' in uri:
            return 'postgresql'
        elif 'sqlite' in uri:
            return 'sqlite'
        return 'unknown'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Config mapping
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}