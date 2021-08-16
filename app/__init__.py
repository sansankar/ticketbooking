from flask import Flask

from .api.route import api

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:ather@localhost:5432/srmTravels"

    migrate = Migrate(app, db)
    db.init_app(app)

    app.register_blueprint(api)

    return app
