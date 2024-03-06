# app/__init__.py

from flask import Flask
from .api.routes import api_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'/*')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root2333@localhost:3306/ttspider'
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app
