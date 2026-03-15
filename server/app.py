from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# Use the exact path from debug-paths
REACT_BUILD_DIR = '/opt/render/project/src/client/build'

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React static files"""
    if not path:
        return send_from_directory(REACT_BUILD_DIR, 'index.html')
    
    # Try to serve the requested file
    try:
        return send_from_directory(REACT_BUILD_DIR, path)
    except:
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)