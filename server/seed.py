from random import choice as rc
from faker import Faker
from app import app
from models import db, User, Task, Assignment
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
fake = Faker()

with app.app_context():
    # Clear existing data
    db.session.query(Assignment).delete()
    db.session.query(Task).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create users
    users = []
    for i in range(5):
        user = User(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password=bcrypt.generate_password_hash("password").decode('utf-8')
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # Create tasks
    tasks = []
    priorities = ["Low", "Medium", "High"]
    for i in range(8):
        task = Task(
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=2),
            priority=rc(priorities),
            completed=fake.boolean(),
            user_id=rc(users).id
        )
        tasks.append(task)
        db.session.add(task)
    db.session.commit()

    # Create assignments (many-to-many)
    for i in range(10):
        assignment = Assignment(
            user_id=rc(users).id,
            task_id=rc(tasks).id,
            completed=fake.boolean(),
            notes=fake.sentence() if fake.boolean() else ""
        )
        db.session.add(assignment)
    db.session.commit()

    print("Seeding complete, Congratulations man!")