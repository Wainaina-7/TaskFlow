from datetime import datetime
from server.extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    tasks = db.relationship("Task", backref="user", lazy=True)
    collaborations = db.relationship("Collaboration", backref="user", lazy=True)
    projects = db.relationship(
        "Project",
        secondary="collaborations",
        backref=db.backref("users", lazy="dynamic", overlaps="collaborations,user"),
        lazy="dynamic",
        overlaps="collaborations,user",
    )


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    tasks = db.relationship("Task", backref="project", lazy=True)
    collaborations = db.relationship(
        "Collaboration",
        backref=db.backref("project", lazy=True, overlaps="projects,users"),
        lazy=True,
        overlaps="projects,users",
    )


class Collaboration(db.Model):

    __tablename__ = "collaborations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    role = db.Column(db.String(50), nullable=False)


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    status = db.Column(db.String(50), nullable=False, default="Pending")
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    category = db.Column(db.String(50), nullable=False, default="General")
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
