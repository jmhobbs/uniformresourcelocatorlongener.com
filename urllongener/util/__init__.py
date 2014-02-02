# -*- coding: utf-8 -*-

import hashlib
import re
from .ip import extract_remote_ip_from_headers


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


def user_fingerprint(request, session):
    '''This is toooootally the best way to identify uniques. /s'''
    if 'fingerprint' not in session:
        user_agent = request.headers.get('HTTP_USER_AGENT', '')
        http_accept = request.headers.get('HTTP_ACCEPT', '')
        accept_language = request.headers.get('HTTP_ACCEPT_LANGUAGE', '')
        accept_encoding = request.headers.get('HTTP_ACCEPT_ENCODING', '')
        ip = extract_remote_ip_from_headers(request.headers)
        session['fingerprint'] = hashlib.sha1("%s %s %s %s %s" % (user_agent, http_accept, accept_language, accept_encoding, ip)).hexdigest()
    return session['fingerprint']
