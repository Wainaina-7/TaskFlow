from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created to avoid circular imports
from routes import register_routes
register_routes(app)

# Serve React frontend - FIXED PATHS
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React static files"""
    build_dir = os.path.join(os.path.dirname(__file__), '../client/build')
    
    # If path is empty it shouldserve index.html, hopefully.
    if not path:
        return send_from_directory(build_dir, 'index.html')
    
    # Try to serve the requested file
    try:
        return send_from_directory(build_dir, path)
    except:
        return send_from_directory(build_dir, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)