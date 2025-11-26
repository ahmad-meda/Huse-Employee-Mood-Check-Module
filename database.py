from flask_sqlalchemy import SQLAlchemy
import os

# Create the SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app"""
    # Database configuration
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:ias12345@localhost:5432/Employee")
    # database_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin%40123@192.168.0.143/huse")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the db with the app
    db.init_app(app)
    
    return db 