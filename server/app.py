from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created to avoid circular imports
from routes import register_routes
register_routes(app)

# Get absolute path to React build folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REACT_BUILD_DIR = os.path.join(BASE_DIR, '..', 'client', 'build')

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React static files"""
    # If path is empty, serve index.html
    if not path:
        return send_from_directory(REACT_BUILD_DIR, 'index.html')
    
    # Try to serve the requested file (JS, CSS, images, etc.)
    requested_file = os.path.join(REACT_BUILD_DIR, path)
    if os.path.exists(requested_file) and os.path.isfile(requested_file):
        return send_from_directory(REACT_BUILD_DIR, path)
    
    # For any other path (like React Router routes), serve index.html
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)