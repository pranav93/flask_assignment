import os

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO') == 'True'
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
DEFAULT_LOGGER_NAME = 'api'

LOGGING_CONFIG = dict(
        version=1,
        formatters={
            'compact': {
                'format': '%(asctime)s [%(levelname)-8.8s] %(name)-10.10s : %(message)s'
            },
            'verbose': {
                'format': '%(asctime)s [%(levelname)-8.8s] %(name)-8.8s [%(filename)-15.15s:%(lineno)-3.3s]: %(message)s'
            },
            'err_report': {
                'format': '%(asctime)s\n%(message)s'
            }
        },
        handlers={
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        loggers={
            '': {
                'handlers': ['default'],
                'level': 'DEBUG'
            },
            'api': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    )
