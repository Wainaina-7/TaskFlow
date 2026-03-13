from flask import request, jsonify
<<<<<<< HEAD
from app import db, bcrypt
from models import User, Task, Assignment

def register_routes(app):

    # user registration and authentication routes
    @app.route("/register", methods=["POST"])
    def register():
        data = request.json
        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            return jsonify({"message": "Login successful", "user_id": user.id})
        return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/users", methods=["GET"])
    def get_users():
        # Get all users (READ action)
        users = User.query.all()
        user_list = []
        for u in users:
            user_list.append({
                "id": u.id,
                "username": u.username,
                "email": u.email
            })
        return jsonify(user_list)

    # task routes
    @app.route("/tasks", methods=["POST"])
    def create_task():
        # Create new task (CREATE action)
        data = request.json
        task = Task(
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            user_id=data["user_id"]
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created"})

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        # Get all tasks (READ action)
        tasks = Task.query.all()
        task_list = []
        for t in tasks:
            task_list.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "priority": t.priority,
                "completed": t.completed,
                "user_id": t.user_id
            })
        return jsonify(task_list)

    @app.route("/tasks/<int:id>", methods=["PATCH"])
    def update_task(id):
        # Update task (UPDATE action)
        task = Task.query.get(id)
        data = request.json
        if "completed" in data:
            task.completed = data["completed"]
=======
from server.app import db, bcrypt
from server.models import User, Task, Project, Collaboration
from datetime import datetime


def register_routes(app):

    # CREATE USER (alias)
    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.json
        if not all(k in data for k in ("username", "email", "password")):
            return jsonify({"error": "username, email, password required"}), 400

        if User.query.filter((User.username == data["username"]) | (User.email == data["email"])) .first():
            return jsonify({"error": "User already exists"}), 409

        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        user = User(username=data["username"], email=data["email"], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created", "user_id": user.id}), 201

    @app.route("/", methods=["GET"])
    def health():
        return jsonify({"status": "TaskFlow backend running", "endpoints": ["/users", "/projects", "/tasks", "/collaborations"]})

    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

    @app.route("/register", methods=["POST"])
    def register():
        return create_user()


    # LOGIN
    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password required"}), 400

        user = User.query.filter_by(email=data["email"]).first()
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            return jsonify({"message": "Login successful", "user_id": user.id})

        return jsonify({"error": "Invalid credentials"}), 401


    # PROJECTS
    @app.route("/projects", methods=["POST"])
    def create_project():
        data = request.json
        if not data or not data.get("title"):
            return jsonify({"error": "Project title required"}), 400

        project = Project(title=data["title"], description=data.get("description", ""))
        db.session.add(project)
        db.session.commit()

        return jsonify({"message": "Project created", "project_id": project.id}), 201

    @app.route("/projects", methods=["GET"])
    def get_projects():
        projects = Project.query.all()
        return jsonify([
            {"id": p.id, "title": p.title, "description": p.description} for p in projects
        ])


    # COLLABORATIONS
    @app.route("/collaborations", methods=["POST"])
    def create_collaboration():
        data = request.json
        if not all(k in data for k in ("user_id", "project_id", "role")):
            return jsonify({"error": "user_id, project_id, role required"}), 400

        if not User.query.get(data["user_id"]):
            return jsonify({"error": "User not found"}), 404
        if not Project.query.get(data["project_id"]):
            return jsonify({"error": "Project not found"}), 404

        collab = Collaboration(user_id=data["user_id"], project_id=data["project_id"], role=data["role"])
        db.session.add(collab)
        db.session.commit()

        return jsonify({"message": "Collaboration added", "collaboration_id": collab.id}), 201

    @app.route("/collaborations", methods=["GET"])
    def get_collaborations():
        collabs = Collaboration.query.all()
        result = []
        for c in collabs:
            result.append({
                "id": c.id,
                "user_id": c.user_id,
                "user": c.user.username if c.user else None,
                "project_id": c.project_id,
                "project": c.project.title if c.project else None,
                "role": c.role,
            })
        return jsonify(result)


    # TASKS
    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.json
        required = ("title", "user_id", "project_id")
        if not all(k in data for k in required):
            return jsonify({"error": "title, user_id, project_id required"}), 400

        if not User.query.get(data["user_id"]):
            return jsonify({"error": "User not found"}), 404
        if not Project.query.get(data["project_id"]):
            return jsonify({"error": "Project not found"}), 404

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

        return jsonify({"message": "Task created", "task_id": task.id}), 201

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        query = Task.query
        user_id = request.args.get("user_id")
        project_id = request.args.get("project_id")
        status = request.args.get("status")
        completed = request.args.get("completed")

        if user_id:
            query = query.filter_by(user_id=int(user_id))
        if project_id:
            query = query.filter_by(project_id=int(project_id))
        if status:
            query = query.filter_by(status=status)
        if completed is not None:
            query = query.filter_by(completed=(completed.lower() == "true"))

        tasks = query.order_by(Task.created_at.desc()).all()

        return jsonify([
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
        ])

    @app.route("/tasks/<int:id>", methods=["GET"])
    def get_task(id):
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({
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
        })

    @app.route("/tasks/<int:id>", methods=["PATCH"])
    def update_task(id):
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        data = request.json
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)
        task.priority = data.get("priority", task.priority)
        task.category = data.get("category", task.category)
        task.completed = data.get("completed", task.completed)

        if data.get("user_id") and User.query.get(data.get("user_id")):
            task.user_id = data["user_id"]

        if data.get("project_id") and Project.query.get(data.get("project_id")):
            task.project_id = data["project_id"]

        if data.get("due_date"):
            task.due_date = datetime.fromisoformat(data["due_date"])

>>>>>>> bce7e116b972be40ba9676c01181d8d6474b5ab4
        db.session.commit()
        return jsonify({"message": "Task updated"})

    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id):
<<<<<<< HEAD
        # Delete task (DELETE action)
        task = Task.query.get(id)
=======
        task = Task.query.get(id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

>>>>>>> bce7e116b972be40ba9676c01181d8d6474b5ab4
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

<<<<<<< HEAD
    # assignment routes for many-to-many relationship between users and tasks
    @app.route("/assignments", methods=["GET"])
    def get_assignments():
        # GET assignemt
        assignments = Assignment.query.all()
        assignment_list = []
        for a in assignments:
            assignment_list.append({
                "id": a.id,
                "user_id": a.user_id,
                "task_id": a.task_id,
                "completed": a.completed,
                "notes": a.notes
            })
        return jsonify(assignment_list)

    @app.route("/assignments", methods=["POST"])
    def create_assignment():
        data = request.json
        assignment = Assignment(
            user_id=data["user_id"],
            task_id=data["task_id"],
            notes=data.get("notes", "")
        )
        db.session.add(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment created"}), 201
=======
    @app.route("/users/<int:user_id>/tasks", methods=["GET"])
    def get_user_tasks(user_id):
        if not User.query.get(user_id):
            return jsonify({"error": "User not found"}), 404

        user_tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        return jsonify([
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
        ])

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

>>>>>>> bce7e116b972be40ba9676c01181d8d6474b5ab4
