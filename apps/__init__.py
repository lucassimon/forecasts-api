# -*- coding: utf-8 -*-

# Python Libs.
from flask import Flask, jsonify
from flask_cors import CORS
# from flask.cli import load_dotenv

# apps

from .db import db
from .celery import celery
from .api import configure_api
from apps.messages import _MSG904


def create_app(testing=False):
    app = Flask('api-forecasts')
    app.config.from_object('configs')
    celery.conf.update(app.config)
    if testing:
        app.config.update(
            MONGODB_HOST=app.config['MONGODB_HOST_TEST']
        )

    @app.errorhandler(404)
    def page_not_found(e):
        resp = jsonify({'status': 404, 'message': _MSG904})
        resp.status_code = 404
        return resp

    CORS(app, resources={r'/*': {'origins': '*'}})

    # Configure MongoEngine
    db.init_app(app)

    # Configure API

    configure_api(app)

    return app
