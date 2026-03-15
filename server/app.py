from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# Absolute path to React build folder - confirmed from debug endpoint
REACT_BUILD_DIR = '/opt/render/project/src/client/build'

# Serve static files from the React build folder
@app.route('/<path:path>')
def serve_static_files(path):
    """Serve any file from the React build directory if it exists."""
    full_path = os.path.join(REACT_BUILD_DIR, path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(REACT_BUILD_DIR, path)
    # If file doesn't exist, let the main route handle it
    return serve_react('')

@app.route('/')
def serve_react(path=''):
    """Serve the main React app."""
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)