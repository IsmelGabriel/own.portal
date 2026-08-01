import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('db_user', '')
db_password = os.getenv('db_password', '')
db_host = os.getenv('db_host', '')
db_port = os.getenv('db_port', '5432')
db_name = os.getenv('db_name', '')
constructed_db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class Config:
    """Base config."""
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-secret')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False

class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = constructed_db_url
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = constructed_db_url
    DEBUG = False
