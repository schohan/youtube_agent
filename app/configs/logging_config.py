import logging
import logging.config


# Define the logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'formatter': 'standard',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 2
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name):
    return logging.getLogger(name)


# Example usage
# logger =  get_logger(__name__) 
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")