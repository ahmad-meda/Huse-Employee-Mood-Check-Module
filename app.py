# from Files.SQLAlchemyModels import SessionLocal
# db = SessionLocal()
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from database import db, init_db

def create_app():
    app = Flask(__name__)
    
    # Initialize database
    init_db(app)
    
    # Initialize migrations
    migrate = Migrate(app, db)
    
    return app
    
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
        #app.run(debug=debug_mode, host='0.0.0.0', port=80)
        app.run(debug=debug_mode, host='0.0.0.0', port=5000)