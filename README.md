# TaskFlow 🚀

A modern, full-stack **project and task management** application built with best practices and contemporary technologies.

## 🎯 Overview

TaskFlow is a clean, professional application designed to help teams manage projects, assign tasks, and collaborate efficiently. It demonstrates a well-structured architecture with a powerful backend API and a beautiful, responsive frontend.

### Key Features
- ✨ **Modern UI** - Built with React, Vite, and Tailwind CSS
- 🎨 **Professional Design** - Clean, intuitive interface with Lucide icons
- 📱 **Responsive** - Works beautifully on desktop, tablet, and mobile
- 🔐 **Secure Authentication** - Password hashing with bcrypt
- 📊 **Project Management** - Create and manage projects
- ✅ **Task Management** - Full CRUD operations for tasks
- 👥 **Collaboration** - Team member management with role-based access
- 🚀 **RESTful API** - Well-documented REST endpoints
- 🗄️ **Database** - PostgreSQL with SQLAlchemy ORM

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - User interface library
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful SVG icon library
- **Formik** - Form state management
- **Yup** - Schema validation
- **React Router** - Client-side routing

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - Cross-origin resource sharing
- **bcrypt** - Password hashing
- **Python 3.8+** - Programming language

### Database
- **PostgreSQL** - Primary production database
- **SQLite** - Development fallback (optional)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16+ and npm
- PostgreSQL (optional for production)
- Git

### Backend Setup

#### 1. Navigate to project root and activate virtual environment
```bash
cd TaskFlow

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

#### 2. Install Python dependencies
```bash
pip install -r server/requirements.txt
```

#### 3. Configure Database

**Option A: PostgreSQL (Recommended)**
```bash
# Create PostgreSQL database and user
sudo -u postgres createuser taskflow_user
sudo -u postgres psql -c "ALTER USER taskflow_user WITH PASSWORD 'your_secure_password';"
sudo -u postgres createdb -O taskflow_user taskflow_db

# Set environment variable
export DATABASE_URL="postgresql://taskflow_user:your_secure_password@localhost:5432/taskflow_db"
```

**Option B: SQLite (Development)**
TaskFlow automatically uses SQLite if `DATABASE_URL` is not set. No additional setup needed!

#### 4. Start the Backend Server
```bash
python server/app.py
```

The backend will run at `http://localhost:5000`

### Frontend Setup

#### 1. Navigate to frontend directory
```bash
cd frontend
```

#### 2. Install dependencies
```bash
npm install
```

#### 3. Start development server
```bash
npm run dev
```

The frontend will run at `http://localhost:5173`

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Response Format
All responses follow a consistent format:
```json
{
  "status": "success|error",
  "message": "Description of the response",
  "data": {}  // Optional data
}
```

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### Login
```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}
```

### User Endpoints

#### Get All Users
```http
GET /users
```

#### Get Specific User
```http
GET /users/:user_id
```

#### Get User's Tasks
```http
GET /users/:user_id/tasks
```

### Project Endpoints

#### Create Project
```http
POST /projects
Content-Type: application/json

{
  "title": "Website Redesign",
  "description": "Redesign company website"
}
```

#### Get All Projects
```http
GET /projects
```

#### Get Specific Project
```http
GET /projects/:project_id
```

#### Delete Project
```http
DELETE /projects/:project_id
```

### Task Endpoints

#### Create Task
```http
POST /tasks
Content-Type: application/json

{
  "title": "Fix login bug",
  "description": "Login not working on mobile",
  "user_id": 1,
  "project_id": 1,
  "status": "In Progress",
  "priority": "High",
  "category": "Bug",
  "completed": false,
  "due_date": "2024-12-31"
}
```

#### Get All Tasks
```http
GET /tasks?user_id=1&project_id=1&status=Pending&completed=false
```

#### Get Specific Task
```http
GET /tasks/:task_id
```

#### Update Task
```http
PATCH /tasks/:task_id
Content-Type: application/json

{
  "status": "Done",
  "completed": true
}
```

#### Delete Task
```http
DELETE /tasks/:task_id
```

### Collaboration Endpoints

#### Add Team Member
```http
POST /collaborations
Content-Type: application/json

{
  "user_id": 1,
  "project_id": 1,
  "role": "Developer"  // Manager, Developer, or Viewer
}
```

#### Get All Collaborations
```http
GET /collaborations
```

#### Get Project Collaborators
```http
GET /projects/:project_id/collaborations
```

#### Remove Team Member
```http
DELETE /collaborations/:collaboration_id
```

---

## 🎨 Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Main layout wrapper
│   │   ├── Navbar.jsx          # Navigation bar with mobile support
│   │   └── ...
│   ├── pages/
│   │   ├── Dashboard.jsx       # Overview and statistics
│   │   ├── Projects.jsx        # Project management
│   │   ├── Tasks.jsx           # Task management
│   │   └── Team.jsx            # Team collaboration
│   ├── App.jsx                 # App router
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles with Tailwind
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🗄️ Backend Structure

```
server/
├── app.py              # Application factory
├── config.py           # Configuration management
├── extensions.py       # Flask extensions
├── models.py           # Database models
├── routes.py           # API routes
└── requirements.txt    # Python dependencies
```

### Database Models

**User**
- Username (unique)
- Email (unique)
- Password (hashed with bcrypt)
- Relationships: tasks, collaborations

**Project**
- Title
- Description
- Relationships: tasks, collaborations

**Task**
- Title, Description
- Status (Pending, In Progress, Done)
- Priority (Low, Medium, High)
- Category
- Completion status
- Due date
- User reference
- Project reference

**Collaboration**
- User reference
- Project reference
- Role (Manager, Developer, Viewer)

---

## 🔒 Security Features

- **Password Hashing** - bcrypt for secure password storage
- **CORS Protection** - Configurable cross-origin resource sharing
- **Input Validation** - Formik and Yup on frontend, Flask validation on backend
- **Error Handling** - Comprehensive error handling and logging
- **Environment Variables** - Sensitive data in `.env` files

### Security Best Practices
- Change `SECRET_KEY` in production
- Use strong database passwords
- Enable HTTPS in production
- Keep dependencies updated
- Implement rate limiting (recommended)
- Add authentication tokens (JWT recommended)

---

## 📦 Development Commands

### Backend
```bash
# Run development server
python server/app.py

# Run with custom configuration
FLASK_ENV=development python server/app.py
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
sudo service postgresql status

# Reset database
python -c "from server.app import create_app; app = create_app(); app.app_context().push(); from server.extensions import db; db.drop_all(); db.create_all()"
```

### Port Already in Use
```bash
# Change Flask port
python server/app.py --port 5001

# Change frontend port in vite.config.js
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r server/requirements.txt --force-reinstall
npm install --legacy-peer-deps
```

---

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy the `dist/` folder
```

### Backend (Heroku/Railway)
```bash
# Set environment variables
heroku config:set DATABASE_URL=postgresql://...

# Deploy
git push heroku main
```

---

## 📝 Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow_db

# Flask
FLASK_ENV=development
SECRET_KEY=your-secure-secret-key

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API endpoint examples

---

## ✨ Future Enhancements

- [ ] Real-time notifications with WebSockets
- [ ] File attachment support
- [ ] Advanced filtering and search
- [ ] Activity timeline
- [ ] Team analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Task templates
- [ ] Recurring tasks

---

**Built with ❤️ for better project management**

4. Start the backend:
   ```bash
   export FLASK_APP=server.app
   flask run
   ```

The backend will run at: `http://localhost:5000`

---

### Frontend (React)

1. Open a new terminal and install dependencies:
   ```bash
   cd TaskFlow/frontend
   npm install
   ```

2. Start the dev server:
   ```bash
   npm run dev -- --port 5173
   ```

The frontend will run at: `http://localhost:5173`

---

## API Endpoints

- `GET /` - health + endpoints list
- `GET /users`, `POST /users`
- `GET /projects`, `POST /projects`
- `GET /tasks`, `POST /tasks`, `PATCH /tasks/:id`, `DELETE /tasks/:id`
- `GET /collaborations`, `POST /collaborations`

---

## Contributing (Wainaina + Mark)

### Backend (Python / Flask)
- Add models and relationships in `server/models.py`
- Add or update endpoints in `server/routes.py`
- Update DB schema using Flask-Migrate migrations

### Frontend (React)
- Update UI in `frontend/src/pages/*`
- Add new routes in `frontend/src/App.jsx`
- Update style in `frontend/src/index.css`

---

## Notes

- The frontend communicates directly with the backend using `http://localhost:5000`.
- If your backend is not reachable, check that PostgreSQL is running and the Flask dev server is up.

---

### Authors
- Wainaina (primary)
- Mark (contributor)
