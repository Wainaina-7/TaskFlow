from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_cors import CORS
<<<<<<< HEAD
from config import Config

# Initialize extensions
=======
from server.config import Config

>>>>>>> bce7e116b972be40ba9676c01181d8d6474b5ab4
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
<<<<<<< HEAD
    app = Flask(__name__) 
    app.config.from_object(Config) 
    
    # Connect extensions to app
    db.init_app(app) 
    migrate.init_app(app, db) 
    bcrypt.init_app(app) 
    CORS(app)
    
    # Register routes
    from routes import register_routes 
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__": 
    app.run(debug=True)
=======
     app = Flask(__name__) 
     app.config.from_object(Config) 
     db.init_app(app) 
     migrate.init_app(app, db) 
     bcrypt.init_app(app) 
     CORS(app)
     from server.routes import register_routes 
     register_routes(app)
     return app

app = create_app()
if __name__ == "__main__": 
     app.run(debug=True)
>>>>>>> bce7e116b972be40ba9676c01181d8d6474b5ab4
