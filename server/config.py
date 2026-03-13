# ALL imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


# Instantiation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking to save memory
app.json.compact = False  

# Define metadata 
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)  
migrate = Migrate(app, db)  # Setting up migrations
db.init_app(app)  # Initialize db with app

# Instantiate REST API for Flask
api = Api(app)

CORS(app)