import argparse
import json
import time
from datetime import datetime

from flask import Flask, g
from orator import Schema

from news.config.config import load_config, register_functions
from news.config.routes import register_routes, FullyQualifiedSource
from news.lib.cache import cache
from news.lib.db.db import db, create_tables
from news.lib.csrf import csrf
from news.lib.login import login_manager
from news.lib.mail import mail
from news.lib.metrics import REQUEST_TIME
from news.lib.sentry import sentry
from news.lib.solr import solr
from news.lib.utils.time_utils import convert_to_timedelta
from news.models.ban import Ban
from news.models.comment import Comment
from news.models.feed import Feed
from news.models.feed_admin import FeedAdmin
from news.models.link import Link
from news.models.report import Report
from news.models.subscriptions import create_subscriptions_table
from news.models.disposable_token import DisposableToken
from news.models.user import User
from news.models.vote import CommentVote, LinkVote
from news.scripts.create_testing_data import importHN, create_stories, loadVotes
from news.scripts.import_fqs import import_fqs


def make_app():
    app = Flask(__name__, static_url_path='/static', static_folder='../static', template_folder='../templates')

    # load config
    load_config(app)

    db.init_app(app)

    solr.init_app(app)

    csrf.init_app(app)

    cache.init_app(app)

    login_manager.init_app(app)

    mail.init_app(app)

    # init sentry only if not in DEBUG mode
    if not app.config['DEBUG']:
        sentry.init_app(app, dsn=app.config['DSN'])

    # register view function and other utilities for templates
    register_functions(app)

    # register all routes
    register_routes(app)

    #cache.clear()
    #archive_links()
    #loadVotes()
    #create_tables(app)

    #from news.scripts.create_testing_data import create_stories
    #create_stories()
    #sentry.init_app(app)
    #importHN()

    #for feed in Feed.get():
    #   feed.commit()

    # with app.app_context():
    #     from news.models.report import Report
    #     Report.create_table()
    #import_fqs()

    print("""eSource news
    Running on URL: {}
    Database: {}
    Redis: {}
    """.format(app.config['NAME'], app.config['ORATOR_DATABASES'][app.config['ORATOR_DATABASES']['default']]['host'], app.config['REDIS']['URL']))

    return app
