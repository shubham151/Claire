from flask import Flask
from app.api.routes import api_blueprint
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Access and set configuration variables
    app.config['12LAB_KEY'] = os.getenv('12LAB_KEY')

    # Register Blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
