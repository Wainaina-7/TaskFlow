from config import create_app, db, bcrypt
from models import User, Task, Assignment
import os
from flask import send_from_directory, jsonify

app = create_app()

# Import routes after app is created
from routes import register_routes
register_routes(app)

# Debug endpoint to check file paths
@app.route('/debug-paths')
def debug_paths():
    """Show what files exist where"""
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(base_dir, '..', 'client', 'build'),
        os.path.join(base_dir, 'client', 'build'),
        '/opt/render/project/src/client/build'
    ]
    
    results = {}
    for path in possible_paths:
        exists = os.path.exists(path)
        index_exists = os.path.exists(os.path.join(path, 'index.html'))
        js_files = []
        css_files = []
        
        if exists:
            static_js = os.path.join(path, 'static', 'js')
            static_css = os.path.join(path, 'static', 'css')
            
            if os.path.exists(static_js):
                js_files = os.listdir(static_js) if os.path.exists(static_js) else []
            if os.path.exists(static_css):
                css_files = os.listdir(static_css) if os.path.exists(static_css) else []
        
        results[path] = {
            'exists': exists,
            'index.html exists': index_exists,
            'js files': js_files,
            'css files': css_files
        }
    
    return jsonify(results)

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React static files"""
    build_dir = os.path.join(os.path.dirname(__file__), '..', 'client', 'build')
    
    if not path:
        return send_from_directory(build_dir, 'index.html')
    
    try:
        return send_from_directory(build_dir, path)
    except:
        return send_from_directory(build_dir, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)