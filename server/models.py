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