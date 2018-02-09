"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from celery import Celery
import docker


db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
cl = Celery()
dkr = docker.from_env()  # NOTE: The docker-machine needs to be pre-configured
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
