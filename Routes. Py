from flask import request, jsonify
from app import db, bcrypt
from models import User, Task


def register_routes(app):

    # REGISTER USER
    @app.route("/register", methods=["POST"])
    def register():

        data = request.json

        hashed_pw = bcrypt.generate_password_hash(
            data["password"]).decode("utf-8")

        user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created"}), 201


    # LOGIN
    @app.route("/login", methods=["POST"])
    def login():

        data = request.json

        user = User.query.filter_by(email=data["email"]).first()

        if user and bcrypt.check_password_hash(user.password, data["password"]):
            return jsonify({"message": "Login successful", "user_id": user.id})

        return jsonify({"error": "Invalid credentials"}), 401


    # CREATE TASK
    @app.route("/tasks", methods=["POST"])
    def create_task():

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


    # GET ALL TASKS
    @app.route("/tasks", methods=["GET"])
    def get_tasks():

        tasks = Task.query.all()

        task_list = []

        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed
            })

        return jsonify(task_list)


    # UPDATE TASK
    @app.route("/tasks/<int:id>", methods=["PATCH"])
    def update_task(id):

        task = Task.query.get(id)

        data = request.json

        task.completed = data.get("completed", task.completed)

        db.session.commit()

        return jsonify({"message": "Task updated"})


    # DELETE TASK
    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id):

        task = Task.query.get(id)

        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted"})
