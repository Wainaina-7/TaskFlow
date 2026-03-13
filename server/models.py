<<<<<<< HEAD
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_bcrypt import Bcrypt
from config import db

bcrypt = Bcrypt()  #password hashing

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-assignments.user', '-tasks.user',)
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    
    # the one to many relationship with tasks and assignments
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Convert to dictionary for JSON response
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'
    
    serialize_rules = ('-user.tasks', '-assignments.task',)
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    priority = db.Column(db.String(20)) 
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # one to many relationship with assignments
    assignments = db.relationship('Assignment', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'user': self.user.username if self.user else None
        }

class Assignment(db.Model, SerializerMixin):
    __tablename__ = 'assignments'
    
    serialize_rules = ('-user.assignments', '-task.assignments',)
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)  
    completed = db.Column(db.Boolean, default=False)  # Extra attribute (user-submittable)
    notes = db.Column(db.String(200))  # Extra attribute (user-submittable)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'completed': self.completed,
            'notes': self.notes,
            'user': self.user.username if self.user else None,
            'task': self.task.title if self.task else None
        }
=======
from server.app import db
from datetime import datetime

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

    tasks = db.relationship("Task", backref="user", lazy=True)
    collaborations = db.relationship("Collaboration", backref="user", lazy=True)
    projects = db.relationship("Project", secondary="collaborations", backref="users", lazy="dynamic")


class Project(db.Model):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    tasks = db.relationship("Task", backref="project", lazy=True)
    collaborations = db.relationship("Collaboration", backref="project", lazy=True)


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
>>>>>>> bce7e11 (added frontend)
