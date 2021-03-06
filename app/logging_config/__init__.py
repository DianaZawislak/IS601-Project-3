import logging
import os
from logging.config import dictConfig

import flask
from flask import request, current_app
from flask_login import current_user

from app.logging_config.log_formatters import RequestFormatter
from app.logging_config.log_formatters import useractivities
from app import config

log_con = flask.Blueprint('log_con', __name__)


# @log_con.before_app_request
# def before_request_logging():
#@log_con.after_app_request

def after_request_song_upload():
    log = logging.getLogger('song_uploads')
    log.info(current_user.email + "  uploaded new songs")


@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response
    return response


@log_con.before_app_first_request
def setup_logs():
    # set the name of the apps log folder to logs
    logdir = config.Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.config.dictConfig(LOGGING_CONFIG)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },

        'useractivities': {
            '()': 'app.logging_config.log_formatters.useractivities',
            'format': '[%(asctime)s] %(levelname)s METHOD: %(request_method)s '
                      'FILENAME:%(filename)s FUNCTION NAME:%(funcName)s() LINE:%(lineno)s] '
                      '%(message)s from %(remote_addr)s'
        }

    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'useractivities',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'useractivities',
            'filename': os.path.join(config.Config.LOG_DIR, 'useractivities.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.dianasapp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'DianasApp.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.request': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'request.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'errors.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.sqlalchemy': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'sqlalchemy.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.werkzeug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'werkzeug.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },

        'file.handler.debugs': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'debugs.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },

        'file.handler.song_uploads': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(config.Config.LOG_DIR, 'song_uploads.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file.handler'],
            'level': 'INFO',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file.handler'],
            'level': 'INFO',
            'propagate': True
        },
        'werkzeug': {  # if __name__ == '__main__'
            'handlers': ['file.handler.werkzeug'],
            'level': 'INFO',
            'propagate': False
        },
        'sqlalchemy.engine': {  # if __name__ == '__main__'
            'handlers': ['file.handler.sqlalchemy'],
            'level': 'INFO',
            'propagate': False
        },
        'dianasapp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.dianasapp'],
            'level': 'INFO',
            'propagate': False
        },
        'myerrors': {  # if __name__ == '__main__'
            'handlers': ['file.handler.errors'],
            'level': 'INFO',
            'propagate': False
        },
        'myrequests': {  # if __name__ == '__main__'
            'handlers': ['file.handler.request'],
            'level': 'DEBUG',
            'propagate': False
        },
        'mydebugs': {  # if __name__ == '__main__'
            'handlers': ['file.handler.debugs'],
            'level': 'INFO',
            'propagate': False
        },

        'song_uploads': {  # if __name__ == '__main__'
            'handlers': ['file.handler.song_uploads'],
            'level': 'INFO',
            'propagate': False
        },

    }
}
