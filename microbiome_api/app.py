from flask import Flask

from microbiome_api import auth, api
from microbiome_api.extensions import db, jwt, cl


def create_app(config=None, testing=False):
    """Application factory, used to create application
    """
    app = Flask('microbiome_api')

    configure_app(app, testing)
    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('microbiome_api.config')

    if testing is True:
        # override with testing config
        app.config.from_object('microbiome_api.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar("MICROBIOME_API_CONFIG", silent=True)


def configure_extensions(app):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)
    cl.config_from_object('microbiome_api.celeryconfig')
    cl.conf.update(app.config)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
