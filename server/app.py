from flask import Flask
from config import app, db, migrate, bcrypt

def create_app():
    from routes import register_routes 
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__": 
    app.run(debug=True)
