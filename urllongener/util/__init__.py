# -*- coding: utf-8 -*-

import random
import re

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
ALPHABET_LEN = len(ALPHABET)


def random_alphanumeric_string(length):
    prefix = []
    for i in xrange(0, length):
        prefix.append(ALPHABET[random.randrange(0, ALPHABET_LEN)])
    return ''.join(prefix)


# Taken from Django via http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
URL_MATCHER = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_valid_url(url):
    return URL_MATCHER.match(url)
