from flask import request, jsonify
from server.extensions import db, bcrypt
from server.models import User, Task, Project, Collaboration
from datetime import datetime
from functools import wraps


def json_required(f):
    """Decorator to ensure request has JSON content."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"status": "error", "message": "Request must be JSON"}), 400
        return f(*args, **kwargs)
    return decorated_function


def success_response(message, data=None, status_code=200):
    """Create a consistent success response."""
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def error_response(message, status_code=400):
    """Create a consistent error response."""
    return jsonify({"status": "error", "message": message}), status_code


def register_routes(app):
    """Register all API routes."""

    # ==================== HEALTH CHECK ====================
    @app.route("/", methods=["GET"])
    def health():
        """Health check endpoint."""
        return success_response(
            "TaskFlow backend is running",
            {
                "version": "1.0.0",
                "endpoints": {
                    "auth": ["/login", "/register"],
                    "users": ["/users", "/users/<id>/tasks"],
                    "projects": ["/projects"],
                    "tasks": ["/tasks"],
                    "collaborations": ["/collaborations"],
                }
            }
        )

    @app.route("/api/health", methods=["GET"])
    def api_health():
        """API health check endpoint."""
        return success_response("API is healthy")

    # ==================== USER ROUTES ====================
    @app.route("/register", methods=["POST"])
    @json_required
    def register():
        """Register a new user."""
        data = request.json
        
        # Validation
        if not all(k in data for k in ("username", "email", "password")):
            return error_response("username, email, and password are required", 400)
        
        # Check for existing user
        if User.query.filter(
            (User.username == data["username"]) | (User.email == data["email"])
        ).first():
            return error_response("User with this username or email already exists", 409)

        # Create user
        try:
            hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            user = User(
                username=data["username"],
                email=data["email"],
                password=hashed_pw
            )
            db.session.add(user)
            db.session.commit()
            
            return success_response(
                "User registered successfully",
                {"user_id": user.id, "username": user.username, "email": user.email},
                201
            )
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            return error_response("Failed to register user", 500)

    @app.route("/login", methods=["POST"])
    @json_required
    def login():
        """User login endpoint."""
        data = request.json
        
        if not data.get("email") or not data.get("password"):
            return error_response("Email and password are required", 400)

        user = User.query.filter_by(email=data["email"]).first()
        
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            return success_response(
                "Login successful",
                {"user_id": user.id, "username": user.username, "email": user.email}
            )

        return error_response("Invalid email or password", 401)

    @app.route("/users", methods=["GET"])
    def get_users():
        """Get all users."""
        users = User.query.all()
        return success_response(
            "Users retrieved successfully",
            [{"id": u.id, "username": u.username, "email": u.email} for u in users]
        )

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        """Get a specific user."""
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        
        return success_response(
            "User retrieved successfully",
            {"id": user.id, "username": user.username, "email": user.email}
        )

    # ==================== PROJECT ROUTES ====================
    @app.route("/projects", methods=["POST"])
    @json_required
    def create_project():
        """Create a new project."""
        data = request.json
        
        if not data.get("title"):
            return error_response("Project title is required", 400)

        try:
            project = Project(
                title=data["title"],
                description=data.get("description", "")
            )
            db.session.add(project)
            db.session.commit()

            return success_response(
                "Project created successfully",
                {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description
                },
                201
            )
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Project creation error: {str(e)}")
            return error_response("Failed to create project", 500)

    @app.route("/projects", methods=["GET"])
    def get_projects():
        """Get all projects."""
        projects = Project.query.all()
        return success_response(
            "Projects retrieved successfully",
            [
                {
                    "id": p.id,
                    "title": p.title,
                    "description": p.description,
                    "task_count": len(p.tasks)
                }
                for p in projects
            ]
        )

    @app.route("/projects/<int:project_id>", methods=["GET"])
    def get_project(project_id):
        """Get a specific project."""
        project = Project.query.get(project_id)
        if not project:
            return error_response("Project not found", 404)

        return success_response(
            "Project retrieved successfully",
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "task_count": len(project.tasks),
                "collaborator_count": len(project.collaborations)
            }
        )

    @app.route("/projects/<int:project_id>", methods=["DELETE"])
    def delete_project(project_id):
        """Delete a project."""
        project = Project.query.get(project_id)
        if not project:
            return error_response("Project not found", 404)

        try:
            # Delete related tasks and collaborations
            Task.query.filter_by(project_id=project_id).delete()
            Collaboration.query.filter_by(project_id=project_id).delete()
            db.session.delete(project)
            db.session.commit()

            return success_response("Project deleted successfully")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Project deletion error: {str(e)}")
            return error_response("Failed to delete project", 500)

    # ==================== TASK ROUTES ====================
    @app.route("/tasks", methods=["POST"])
    @json_required
    def create_task():
        """Create a new task."""
        data = request.json
        
        required_fields = ("title", "user_id", "project_id")
        if not all(k in data for k in required_fields):
            return error_response(f"Required fields: {', '.join(required_fields)}", 400)

        # Validate user and project exist
        if not User.query.get(data["user_id"]):
            return error_response("User not found", 404)
        if not Project.query.get(data["project_id"]):
            return error_response("Project not found", 404)

        try:
            task = Task(
                title=data["title"],
                description=data.get("description", ""),
                status=data.get("status", "Pending"),
                priority=data.get("priority", "Medium"),
                category=data.get("category", "General"),
                completed=data.get("completed", False),
                due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
                user_id=data["user_id"],
                project_id=data["project_id"],
            )
            db.session.add(task)
            db.session.commit()

            return success_response(
                "Task created successfully",
                {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status
                },
                201
            )
        except ValueError:
            return error_response("Invalid date format. Use ISO format (YYYY-MM-DD)", 400)
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Task creation error: {str(e)}")
            return error_response("Failed to create task", 500)

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        """Get all tasks with optional filtering."""
        query = Task.query
        
        # Apply filters
        if request.args.get("user_id"):
            query = query.filter_by(user_id=int(request.args.get("user_id")))
        if request.args.get("project_id"):
            query = query.filter_by(project_id=int(request.args.get("project_id")))
        if request.args.get("status"):
            query = query.filter_by(status=request.args.get("status"))
        if request.args.get("completed"):
            query = query.filter_by(completed=(request.args.get("completed").lower() == "true"))

        tasks = query.order_by(Task.created_at.desc()).all()

        return success_response(
            "Tasks retrieved successfully",
            [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "status": t.status,
                    "priority": t.priority,
                    "category": t.category,
                    "completed": t.completed,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "created_at": t.created_at.isoformat(),
                    "user_id": t.user_id,
                    "project_id": t.project_id,
                }
                for t in tasks
            ]
        )

    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        """Get a specific task."""
        task = Task.query.get(task_id)
        if not task:
            return error_response("Task not found", 404)

        return success_response(
            "Task retrieved successfully",
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "category": task.category,
                "completed": task.completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "user_id": task.user_id,
                "project_id": task.project_id,
            }
        )

    @app.route("/tasks/<int:task_id>", methods=["PATCH"])
    @json_required
    def update_task(task_id):
        """Update a task."""
        task = Task.query.get(task_id)
        if not task:
            return error_response("Task not found", 404)

        data = request.json
        
        try:
            # Update fields if provided
            if "title" in data:
                task.title = data["title"]
            if "description" in data:
                task.description = data["description"]
            if "status" in data:
                task.status = data["status"]
            if "priority" in data:
                task.priority = data["priority"]
            if "category" in data:
                task.category = data["category"]
            if "completed" in data:
                task.completed = data["completed"]
            if "due_date" in data:
                task.due_date = datetime.fromisoformat(data["due_date"]) if data["due_date"] else None
            if "user_id" in data:
                if User.query.get(data["user_id"]):
                    task.user_id = data["user_id"]
                else:
                    return error_response("User not found", 404)
            if "project_id" in data:
                if Project.query.get(data["project_id"]):
                    task.project_id = data["project_id"]
                else:
                    return error_response("Project not found", 404)

            db.session.commit()
            return success_response("Task updated successfully")
        except ValueError:
            return error_response("Invalid date format. Use ISO format (YYYY-MM-DD)", 400)
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Task update error: {str(e)}")
            return error_response("Failed to update task", 500)

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        """Delete a task."""
        task = Task.query.get(task_id)
        if not task:
            return error_response("Task not found", 404)

        try:
            db.session.delete(task)
            db.session.commit()
            return success_response("Task deleted successfully")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Task deletion error: {str(e)}")
            return error_response("Failed to delete task", 500)

    @app.route("/users/<int:user_id>/tasks", methods=["GET"])
    def get_user_tasks(user_id):
        """Get all tasks for a specific user."""
        if not User.query.get(user_id):
            return error_response("User not found", 404)

        user_tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        
        return success_response(
            "User tasks retrieved successfully",
            [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "status": t.status,
                    "priority": t.priority,
                    "category": t.category,
                    "completed": t.completed,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "created_at": t.created_at.isoformat(),
                    "project_id": t.project_id,
                }
                for t in user_tasks
            ]
        )

    # ==================== COLLABORATION ROUTES ====================
    @app.route("/collaborations", methods=["POST"])
    @json_required
    def create_collaboration():
        """Create a collaboration (add member to project)."""
        data = request.json
        
        required_fields = ("user_id", "project_id", "role")
        if not all(k in data for k in required_fields):
            return error_response(f"Required fields: {', '.join(required_fields)}", 400)

        # Validate references
        if not User.query.get(data["user_id"]):
            return error_response("User not found", 404)
        if not Project.query.get(data["project_id"]):
            return error_response("Project not found", 404)

        try:
            collab = Collaboration(
                user_id=data["user_id"],
                project_id=data["project_id"],
                role=data["role"]
            )
            db.session.add(collab)
            db.session.commit()

            return success_response(
                "Collaboration created successfully",
                {"id": collab.id, "role": collab.role},
                201
            )
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Collaboration creation error: {str(e)}")
            return error_response("Failed to create collaboration", 500)

    @app.route("/collaborations", methods=["GET"])
    def get_collaborations():
        """Get all collaborations."""
        collabs = Collaboration.query.all()
        
        return success_response(
            "Collaborations retrieved successfully",
            [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "user": c.user.username if c.user else None,
                    "project_id": c.project_id,
                    "project": c.project.title if c.project else None,
                    "role": c.role,
                }
                for c in collabs
            ]
        )

    @app.route("/collaborations/<int:collab_id>", methods=["DELETE"])
    def delete_collaboration(collab_id):
        """Delete a collaboration."""
        collab = Collaboration.query.get(collab_id)
        if not collab:
            return error_response("Collaboration not found", 404)

        try:
            db.session.delete(collab)
            db.session.commit()
            return success_response("Collaboration deleted successfully")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Collaboration deletion error: {str(e)}")
            return error_response("Failed to delete collaboration", 500)

    @app.route("/projects/<int:project_id>/collaborations", methods=["GET"])
    def get_project_collaborations(project_id):
        """Get all collaborators for a project."""
        if not Project.query.get(project_id):
            return error_response("Project not found", 404)

        collabs = Collaboration.query.filter_by(project_id=project_id).all()
        
        return success_response(
            "Project collaborations retrieved successfully",
            [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "user": c.user.username if c.user else None,
                    "role": c.role,
                }
                for c in collabs
            ]
        )

    @app.route("/dashboard/<int:user_id>/summary", methods=["GET"])
    def dashboard_summary(user_id):
        if not User.query.get(user_id):
            return jsonify({"error": "User not found"}), 404

        total = Task.query.filter_by(user_id=user_id).count()
        completed = Task.query.filter_by(user_id=user_id, completed=True).count()
        pending = total - completed
        priorities = db.session.query(Task.priority, db.func.count(Task.id)).filter_by(user_id=user_id).group_by(Task.priority).all()
        categories = db.session.query(Task.category, db.func.count(Task.id)).filter_by(user_id=user_id).group_by(Task.category).all()

        return jsonify({
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "tasks_by_priority": {p: c for p, c in priorities},
            "tasks_by_category": {c: cnt for c, cnt in categories},
        })

