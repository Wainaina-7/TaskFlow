from config import create_app, db, bcrypt
from models import User, Task, Assignment

app = create_app()

# Import routes after app is created to avoid circular imports
from routes import register_routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
