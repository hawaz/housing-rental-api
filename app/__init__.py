from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints 
    from .routes import main
    app.register_blueprint(main)
    print("DB URI in use:", app.config["SQLALCHEMY_DATABASE_URI"])


    return app
