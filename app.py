from flask import Flask
from flask_sqlalchemyimport SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
     app = Flask(__name__) 
     app.config.from_object(Config) 
     db.init_app(app) 
     migrate.init_app(app, db) 
     bcrypt.init_app(app) 
     CORS(app)
     from routes import register_routes 
     register_routes(app)
     return app

app = create_app()
if __name__ == "__main__": 
     app.run(debug=True)