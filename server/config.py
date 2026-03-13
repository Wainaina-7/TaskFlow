<<<<<<< HEAD
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData
=======
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
>>>>>>> 4ec118b6979bc87de68fe61e1ab8ea7a64074465

# Initialize extensions
bcrypt = Bcrypt()

<<<<<<< HEAD
# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  

# Setup database
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)  
migrate = Migrate(app, db)
db.init_app(app)

CORS(app)
=======
class Config:
    # Postgres is the preferred default for TaskFlow.
    # You can override this by setting DATABASE_URL to any valid SQLAlchemy database URI.
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "taskflow_db")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        if POSTGRES_PASSWORD:
            SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
            )
        else:
            SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{POSTGRES_USER}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
            )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
>>>>>>> 4ec118b6979bc87de68fe61e1ab8ea7a64074465
