import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-development-only'
    EXA_API_KEY = os.environ.get(
        'EXA_API_KEY')

    # GitHub search settings
    GITHUB_API_URL = 'https://api.github.com'

    # Application settings
    DEBUG = False
    TESTING = False

    # Results per page
    RESULTS_PER_PAGE = 10


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True


class ProductionConfig(Config):
    """Production configuration."""
    # Production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    EXA_API_KEY = os.environ.get('EXA_API_KEY')  # Must be set in production


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Return the appropriate configuration object based on the environment."""
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    return config[config_name]
