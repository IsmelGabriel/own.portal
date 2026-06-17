import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """
    Configures the application logger.
    Logs will be output to both the console and a rotating file.
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Formatting
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s (%(lineno)d): %(message)s'
    )

    # File Handler
    file_handler = RotatingFileHandler(
        'logs/own_portal.log',
        maxBytes=10240000, # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Set up root logger so getLogger(__name__) works everywhere
    root_logger = logging.getLogger()

    # Remove existing handlers to avoid duplicates during dev reload
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Set Flask's app.logger handlers
    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False

    app.logger.info('Logging system initialized.')
