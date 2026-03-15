from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# Define the path to the React build directory
REACT_BUILD_DIR = '/opt/render/project/src/client/build'

# Serve static files explicitly
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images) from the React build folder."""
    return send_from_directory(os.path.join(REACT_BUILD_DIR, 'static'), filename)

# Serve the main React app and handle all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve the React app's index.html for all non-static routes."""
    # If the path is not empty and is not a static file request, serve index.html
    # This allows React Router to handle client-side routing.
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)