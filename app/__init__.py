import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import sys
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


def configure_logging(app):
    """Configure logging for the application."""
    # Set up basic configuration
    log_level = logging.DEBUG if app.debug else logging.INFO

    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # File handler (if in production)
    if not app.debug:
        # Ensure log directory exists
        log_dir = os.path.join(app.instance_path, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'exahub.log'),
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)

    # Log application startup
    app.logger.info('ExaHub starting up')


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        GITHUB_TOKEN=os.environ.get('GITHUB_TOKEN'),
        EXA_API_KEY=os.environ.get('EXA_API_KEY'),
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Load test config if provided
    if test_config is not None:
        app.config.from_mapping(test_config)
    # Otherwise, load the instance config if it exists
    else:
        app.config.from_pyfile('config.py', silent=True)

    # Configure logging
    configure_logging(app)

    # Log configuration status
    app.logger.info(
        f"Starting with GitHub token: {'configured' if app.config.get('GITHUB_TOKEN') else 'missing'}")
    app.logger.info(
        f"Starting with Exa API key: {'configured' if app.config.get('EXA_API_KEY') else 'missing'}")

    # Initialize extensions
    csrf.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from exa_github_search.app.routes import main, search, api
    app.register_blueprint(main.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(api.bp)

    # Make url_for('index') work for the index page
    app.add_url_rule('/', endpoint='index')

    return app
