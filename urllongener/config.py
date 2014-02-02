# -*- coding: utf-8 -*-


class BaseConfig(object):
    ENV = 'PRODUCTION'

    DEBUG = False
    TESTING = False

    TIMEZONE = "UTC"

    REDIS_URL = 'redis://localhost:6379/0'

    UPLOAD_DESTINATION = 'local'

    AWS_ACCESS_KEY = None
    AWS_SECRET_KEY = None
    S3_BUCKET = None
    UPLOAD_URL_FORMAT_STRING = None

    # Max POST request size
    MAX_CONTENT_LENGTH = int(6.25 * 1024 * 1024)  # 6MB uploads + breathing room

    # Size in pixels to crop images
    LONGEST_SIDE = 400


class TestConfig(BaseConfig):
    ENV = 'TESTING'

    TESTING = True
    CSRF_ENABLED = False

    REDIS_URL = 'redis://localhost:6379/15'
