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

# Serve static files (CSS, JS, images)
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the React build/static folder."""
    return send_from_directory(os.path.join(REACT_BUILD_DIR, 'static'), filename)

# Serve the main React app for all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve index.html for any non-static route."""
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)