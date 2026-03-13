from flask import request, jsonify
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
        db.session.commit()
        return jsonify({"message": "Task updated"})

    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id):
        # Delete task (DELETE action)
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

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