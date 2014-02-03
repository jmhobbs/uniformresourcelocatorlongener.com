# -*- coding: utf-8 -*-

import hashlib
import urlparse

import time
from datetime import datetime
from pytz import timezone

from flask import request, render_template, send_from_directory, abort, url_for, redirect, session

from .util import is_valid_url, user_fingerprint
from .util.ip import extract_remote_ip_from_headers
from .extensions import redis


def register_views(app):
    APP_TZ = timezone(app.config.get('TIMEZONE', 'UTC'))

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
                pipe = redis.pipeline()
                pipe.set("urlongener:%s:url" % slug, url)
                pipe.set("urlongener:%s:created" % slug, time.time())
                pipe.set("urlongener:%s:originip" % slug, extract_remote_ip_from_headers(request.headers))

                dt = datetime.fromtimestamp(time.time())
                dt = APP_TZ.localize(dt)

                pipe.incr('urlongener:stats:created')
                pipe.incr('urlongener:stats:created:%d' % (dt.year,))
                pipe.incr('urlongener:stats:created:%d-%02d' % (dt.year, dt.month))
                pipe.incr('urlongener:stats:created:%d-%02d-%02d' % (dt.year, dt.month, dt.day))

                pipe.execute()

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

        parsed = urlparse.urlparse(url)
        deeper = parsed.netloc.lower() == app.config.get('SERVER_NAME', '').lower()

        created = float(redis.get("urlongener:%s:created" % slug) or 0)
        created = datetime.fromtimestamp(created)
        created = APP_TZ.localize(created)

        uniques_all_time = int(redis.scard('urllongener:%s:uniques' % slug) or 0)
        redirects_all_time = int(redis.get('urllongener:%s:stats:redirects' % slug) or 0)

        return render_template('view.html', url=url, slug=slug, created=created, uniques_all_time=uniques_all_time, redirects_all_time=redirects_all_time, deeper=deeper)

    @app.route('/<slug>')
    def do_redirect(slug):
        url = redis.get('urlongener:%s:url' % slug)
        if not url:
            return abort(404)

        fingerprint = user_fingerprint(request, session)

        dt = datetime.fromtimestamp(time.time())
        dt = APP_TZ.localize(dt)

        pipe = redis.pipeline()
        pipe.incr('urllongener:stats:redirects')
        pipe.incr('urllongener:stats:redirects:%d' % dt.year)
        pipe.incr('urllongener:stats:redirects:%d-%02d' % (dt.year, dt.month))
        pipe.incr('urllongener:stats:redirects:%d-%02d-%02d' % (dt.year, dt.month, dt.day))

        pipe.incr('urllongener:%s:stats:redirects' % slug)
        pipe.incr('urllongener:%s:stats:redirects:%d' % (slug, dt.year,))
        pipe.incr('urllongener:%s:stats:redirects:%d-%02d' % (slug, dt.year, dt.month))
        pipe.incr('urllongener:%s:stats:redirects:%d-%02d-%02d' % (slug, dt.year, dt.month, dt.day))

        pipe.sadd('urllongener:%s:uniques' % slug, fingerprint)
        pipe.sadd('urllongener:%s:uniques:%d' % (slug, dt.year), fingerprint)
        pipe.sadd('urllongener:%s:uniques:%d-%02d' % (slug, dt.year, dt.month), fingerprint)
        pipe.sadd('urllongener:%s:uniques:%d-%02d-%02d' % (slug, dt.year, dt.month, dt.day), fingerprint)
        pipe.execute()

        return redirect(url)
