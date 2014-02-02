# -*- coding: utf-8 -*-

import hashlib
import time

from flask import request, render_template, send_from_directory, abort, url_for, redirect

from .util import is_valid_url
from .util.ip import extract_remote_ip_from_headers
from .extensions import redis


def register_views(app):

    #####################################################
    # Util and static. Override these in nginx where possible.

    @app.route('/robots.txt')
    @app.route('/humans.txt')
    @app.route('/favicon.ico')
    def root_level_static_files():
        return send_from_directory(app.static_folder, request.path[1:])

    #####################################################
    # App!
    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            url = request.form.get('url', '').strip()
            if not is_valid_url(url):
                return render_template('index.html', error=True, url=url)

            url_length = len(url)

            new_url = 'http://uniformresourcelocatorlongener.com/'
            base_length = len(new_url)

            slug = hashlib.sha1(url + "herpderp").hexdigest()

            while base_length + len(slug) < url_length:
                slug += hashlib.sha1(url + "herpderp" + slug).hexdigest()

            if not redis.get('urlongener:%s:url' % slug):
                # TODO: Check for collisions
                redis.set("urlongener:%s:url" % slug, url)
                redis.set("urlongener:%s:created" % slug, time.time())
                redis.set("urlongener:%s:originip" % slug, extract_remote_ip_from_headers(request.headers))

            return redirect(url_for("view", slug=slug))

        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/_/<slug>')
    def view(slug):
        url = redis.get('urlongener:%s:url' % slug)
        if not url:
            return abort(404)
        return render_template('view.html', url=url, slug=slug)

    @app.route('/<slug>')
    def do_redirect(slug):
        url = redis.get('urlongener:%s:url' % slug)
        if url:
            # TODO: Stats
            return redirect(url)
        return abort(404)
