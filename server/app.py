from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# The confirmed path to the React build folder
REACT_BUILD_DIR = '/opt/render/project/src/client/build'

# Serve ANY file from the build folder
@app.route('/<path:path>')
def serve_all_files(path):
    """Serve any file from the build directory."""
    full_path = os.path.join(REACT_BUILD_DIR, path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(REACT_BUILD_DIR, path)
    # If not a file, serve index.html
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

@app.route('/')
def serve_root():
    """Serve index.html for root path."""
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)