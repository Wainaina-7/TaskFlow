from flask import Flask
<<<<<<< HEAD
from config import app, db, migrate, bcrypt

def create_app():
    from routes import register_routes 
    register_routes(app)
=======
from flask_cors import CORS
from server.config import Config
from server.extensions import db, migrate, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    CORS(app)

    from server.routes import register_routes
    register_routes(app)

    # For local dev, ensure the database tables exist so the API can start without manual migrations.
    # This is safe for SQLite and helps avoid "no such table" errors during development.
    with app.app_context():
        db.create_all()

>>>>>>> 4ec118b6979bc87de68fe61e1ab8ea7a64074465
    return app

app = create_app()

if __name__ == "__main__": 
    app.run(debug=True)
