from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Extension instances are created here to avoid circular imports.
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
