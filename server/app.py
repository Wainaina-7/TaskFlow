from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# Get the absolute path to the React build folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REACT_BUILD_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'client', 'build'))

print(f"Serving React from: {REACT_BUILD_DIR}", flush=True)

# Serve static files (CSS, JS, images)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(REACT_BUILD_DIR, 'static'), filename)

# Serve the main React app for all other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)