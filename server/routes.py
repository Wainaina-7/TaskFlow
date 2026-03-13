from flask import request, jsonify
from models import User, Task, Assignment
from config import db, bcrypt

def register_routes(app):
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
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.json
        task = Task(
            title=data["title"],
            description=data["description"],
            priority=data.get("priority", "Medium"),
            user_id=data["user_id"]
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created"})

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route("/tasks/<int:id>", methods=["PATCH"])
    def update_task(id):
        task = Task.query.get(id)
        data = request.json
        if "completed" in data:
            task.completed = data["completed"]
        if "priority" in data:
            task.priority = data["priority"]
        db.session.commit()
        return jsonify({"message": "Task updated"})

    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id):
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

    @app.route("/assignments", methods=["GET"])
    def get_assignments():
        assignments = Assignment.query.all()
        return jsonify([a.to_dict() for a in assignments])

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

    @app.route("/assignments/<int:id>", methods=["PATCH"])
    def update_assignment(id):
        assignment = Assignment.query.get(id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404
        
        data = request.json
        if "completed" in data:
            assignment.completed = data["completed"]
        if "notes" in data:
            assignment.notes = data["notes"]
        
        db.session.commit()
        return jsonify({"message": "Assignment updated"}), 200

    @app.route("/assignments/<int:id>", methods=["DELETE"])
    def delete_assignment(id):
        assignment = Assignment.query.get(id)
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({"message": "Assignment deleted"}), 200
