from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# DEBUG ROUTE - Add this to see what files exist
@app.route('/debug-ls')
def debug_ls():
    import subprocess
    result = {}
    
    build_path = '/opt/render/project/src/client/build'
    result['build_exists'] = os.path.exists(build_path)
    
    if result['build_exists']:
        try:
            result['build_contents'] = subprocess.getoutput(f'ls -la {build_path}')
            result['static_contents'] = subprocess.getoutput(f'ls -la {build_path}/static')
            if os.path.exists(f'{build_path}/static/css'):
                result['css_contents'] = subprocess.getoutput(f'ls -la {build_path}/static/css')
            if os.path.exists(f'{build_path}/static/js'):
                result['js_contents'] = subprocess.getoutput(f'ls -la {build_path}/static/js')
        except Exception as e:
            result['error'] = str(e)
    
    output = f"Build path exists: {result.get('build_exists')}\n\n"
    output += f"Build contents:\n{result.get('build_contents', 'N/A')}\n\n"
    output += f"Static contents:\n{result.get('static_contents', 'N/A')}\n\n"
    output += f"CSS contents:\n{result.get('css_contents', 'N/A')}\n\n"
    output += f"JS contents:\n{result.get('js_contents', 'N/A')}"
    
    return f"<pre>{output}</pre>"

# Absolute path to React build folder - confirmed from debug endpoint
REACT_BUILD_DIR = '/opt/render/project/src/client/build'

# Serve static files from the React build folder
@app.route('/<path:path>')
def serve_static_files(path):
    """Serve any file from the React build directory."""
    # Try to serve the requested file directly
    try:
        return send_from_directory(REACT_BUILD_DIR, path)
    except:
        # If the file isn't found, let the main route handle it
        return serve_react('')

@app.route('/')
def serve_react(path=''):
    """Serve the main React app's index.html for all other routes."""
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)