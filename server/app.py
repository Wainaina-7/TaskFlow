import os
from flask import Flask, jsonify
from flask_cors import CORS
from server.config import config
from server.extensions import db, migrate, bcrypt

def create_app(config_name=None):
    """Application factory for creating Flask app instance."""
    
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, "development"))
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Register error handlers
    register_error_handlers(app)
    
    # Register routes
    from server.routes import register_routes
    register_routes(app)

    # Create database tables (for development/testing)
    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"status": "error", "message": "Bad request", "code": 400}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Resource not found", "code": 404}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"status": "error", "message": "Internal server error", "code": 500}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unhandled exceptions."""
        db.session.rollback()
        app.logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred",
            "code": 500
        }), 500


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", True), host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))