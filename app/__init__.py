from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Initialize MongoDB connection
    client = MongoClient(os.getenv('MONGODB_URI'))
    app.db = client.f1_predictor
    
    # Register blueprints
    from app.routes import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    
    return app 