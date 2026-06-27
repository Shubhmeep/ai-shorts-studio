from flask import Flask

from app.config import Config
from app.extensions import db, migrate
from app.routes import main


# app factory pattern.
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # This connects SQLAlchemy and migrations to the Flask app.
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    app.register_blueprint(main)

    return app
