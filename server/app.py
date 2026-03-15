from config import create_app, db, bcrypt
from models import User, Task, Assignment

app = create_app()

# Import routes after app is created to avoid circular imports
from routes import register_routes
register_routes(app)

# minor change to test deployment
import os
from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React static files"""
    if path and os.path.exists(os.path.join('../client/build', path)):
        return send_from_directory('../client/build', path)
    return send_from_directory('../client/build', 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
