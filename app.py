from flask import Flask
from flask_sqlalchemyimport SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_cors import CORS
from config import Config