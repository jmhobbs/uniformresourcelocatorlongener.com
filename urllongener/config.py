# -*- coding: utf-8 -*-


class BaseConfig(object):
    ENV = 'PRODUCTION'

    DEBUG = False
    TESTING = False

    TIMEZONE = "UTC"

    REDIS_URL = 'redis://localhost:6379/0'

    MAX_CONTENT_LENGTH = 102400

    SESSION_COOKIE_NAME = 'loooooooooong'
    PERMANENT_SESSION_LIFETIME = 31536000  # 1 Year session


class TestConfig(BaseConfig):
    ENV = 'TESTING'

    TESTING = True
    CSRF_ENABLED = False

    REDIS_URL = 'redis://localhost:6379/15'
