# TaskFlow 

## Description
TaskFlow is a task management application that allows teams to create tasks, assign them to multiple users, and track progress. Kind of like a mini- kanban app.

## Features
- User registration and login
- Create, edit, and delete tasks
- Assign tasks to multiple users
- Mark assignments as complete
- Add personal notes to assignments
- View all tasks, users, and assignments

## Tech Stack
- **Backend**: Flask, SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-CORS
- **Frontend**: React, React Router, Formik, Yup
- **Database**: SQLite (development), PostgreSQL (production)

## Installation

### Backend Setup
```bash
# After cloning the repository to your local machine, navigate to server directory.
cd server

# Install dependencies
pipenv install

# Enter the virtual environment
pipenv shell

# Set up the database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# Run server
python app.py
```

### Frontend Setup
```bash
# In a new terminal, navigate to client file within the project folder.
cd client

# Install dependencies
npm install

# Start React app
npm start
```
The app should start up at http://localhost:3000

## API Routes
### Users
GET /users - Get all users

POST /register - Create new user

POST /login - User login

### Tasks
GET /tasks - Get all tasks

POST /tasks - Create new task

PATCH /tasks/<id> - Update task

DELETE /tasks/<id> - Delete task

### Assignments
GET /assignments - Get all assignments

POST /assignments - Create new assignment

PATCH /assignments/<id> - Update assignment

DELETE /assignments/<id> - Delete assignment.

## Validation
All forms use Formik for handling

### Yup validation includes:
- Required field validation
- Minimum/maximum length validation
- Email format validation