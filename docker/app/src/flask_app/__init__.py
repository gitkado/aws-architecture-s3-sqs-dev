#!/usr/bin/env python
# coding: utf-8

from logging.config import dictConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from .consts import LOG_DICT_CONFIG, FLASK_CONFIG_LIST, CONFIG_NAME


# logger
dictConfig(LOG_DICT_CONFIG)

app = Flask(__name__)
app.config.from_object(FLASK_CONFIG_LIST[CONFIG_NAME])

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

import flask_app.views
