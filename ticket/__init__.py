from flask import Flask
from .api.router import api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ather@localhost:5432/Travels'
    
    from .model import db
    migrate = Migrate(app, db)
    db.init_app(app)

    app.register_blueprint(api)
  
    return app