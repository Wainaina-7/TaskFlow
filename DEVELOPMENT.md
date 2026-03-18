# Development Setup Guide

Complete guide for setting up TaskFlow for development.

## 🛠️ Prerequisites

- **Python 3.8+** - Download from [python.org](https://python.org)
- **Node.js 16+** - Download from [nodejs.org](https://nodejs.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **PostgreSQL** (optional) - Download from [postgresql.org](https://postgresql.org)
- **VS Code** (recommended) - Download from [code.visualstudio.com](https://code.visualstudio.com)

## 📋 Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/Taskflow.git
cd Taskflow
```

### Step 2: Backend Setup

#### Create Virtual Environment
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
python -m venv venv
venv\Scripts\activate.bat
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r server/requirements.txt
```

#### Create .env File
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Database Setup (Optional - Use SQLite for quick start)

**Option 1: SQLite (Default)**
- No setup needed! TaskFlow uses SQLite by default

**Option 2: PostgreSQL**
```bash
# Linux
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# macOS with Homebrew
brew install postgresql@15
brew services start postgresql@15@

# Then create database
createdb taskflow_db
# Or with password authentication
createdb -U postgres taskflow_db
```

Then set in `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/taskflow_db
```

### Step 3: Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Verify Setup
```bash
npm run build  # Check if build works
```

## 🚀 Running the Application

### Terminal 1: Backend
```bash
# Make sure you're in the root directory
source venv/bin/activate  # or venv\Scripts\activate on Windows
python server/app.py
```
- ✅ Backend ready at `http://localhost:5000`
- Check: Visit `http://localhost:5000/` should show health check

### Terminal 2: Frontend
```bash
# In a new terminal, navigate to project root
cd frontend
npm run dev
```
- ✅ Frontend ready at `http://localhost:5173`
- The browser should auto-open to http://localhost:5173

## 🧪 Testing the Application

1. **Create Account**
   - Go to `http://localhost:5173`
   - Click Register
   - Enter username, email, password
   - Click Register

2. **Test Features**
   - Create a project on Projects page
   - Create a task on Tasks page
   - Add team members on Team page
   - View statistics on Dashboard

3. **Test API**
   ```bash
   # Get all users
   curl http://localhost:5000/users

   # Get all projects
   curl http://localhost:5000/projects

   # Get health check
   curl http://localhost:5000/
   ```

## 🎨 VS Code Setup (Recommended)

### Recommended Extensions
1. **Python**
   - Publisher: Microsoft
   - ID: `ms-python.python`

2. **Pylance**
   - Publisher: Microsoft
   - ID: `ms-python.vscode-pylance`

3. **ES7+ React/Redux/React-Native snippets**
   - Publisher: dsznajder
   - ID: `dsznajder.es7-react-js-snippets`

4. **Prettier - Code formatter**
   - Publisher: Prettier
   - ID: `esbenp.prettier-vscode`

5. **Tailwind CSS IntelliSense**
   - Publisher: bradlc
   - ID: `bradlc.vscode-tailwindcss`

### VS Code Settings
Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/venv": true,
    "**/node_modules": true
  }
}
```

### VS Code Launch Configuration
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "server/app.py",
        "FLASK_ENV": "development"
      },
      "args": ["run", "--port", "5000"],
      "jinja": true,
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

## 📚 Project Structure

```
Taskflow/
├── frontend/                 # React + Vite
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── App.jsx          # Main app component
│   │   └── index.css        # Global styles
│   ├── vite.config.js       # Vite configuration
│   ├── tailwind.config.js   # Tailwind configuration
│   ├── postcss.config.js    # PostCSS configuration
│   └── package.json
│
├── server/                  # Flask backend
│   ├── app.py              # Application factory
│   ├── config.py           # Configuration
│   ├── models.py           # Database models
│   ├── routes.py           # API routes
│   ├── extensions.py       # Flask extensions
│   └── requirements.txt    # Python dependencies
│
├── migrations/             # Database migrations (Alembic)
├── venv/                   # Virtual environment (auto-created)
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── CONTRIBUTING.md         # Contributing guidelines
├── QUICKSTART.md           # Quick start guide
└── MODERNIZATION.md        # Modernization details
```

## 🐛 Troubleshooting

### Python Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
python server/app.py --port 5001
```

### Module Not Found
```bash
# Ensure you're in virtual environment
which python  # Should show venv path

# Reinstall dependencies
pip install -r server/requirements.txt --force-reinstall
```

### Database Issues
```bash
# Reset database (will lose data)
# For SQLite
rm taskflow.db

# For PostgreSQL
dropdb taskflow_db
createdb taskflow_db
```

### npm Dependencies
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## 🔄 Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Backend: Edit files in `server/`
   - Frontend: Edit files in `frontend/src/`

3. **Test Your Changes**
   - Backend: Test API endpoints with curl
   - Frontend: Check browser for UI changes

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: Your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature
   ```

## 📖 Useful Commands

### Backend
```bash
# Run server with debug
FLASK_ENV=development python server/app.py

# Run with different config
FLASK_ENV=testing python server/app.py

# Initialize database
python -c "from server.app import create_app; app = create_app(); app.app_context().push(); from server.extensions import db; db.create_all()"
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Format code
npm run format  # if ESLint is configured
```

## 🚀 Next Steps

1. Read the [README.md](README.md) for full documentation
2. Check [QUICKSTART.md](QUICKSTART.md) for quick guide
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
4. Explore [API endpoints](README.md#-api-documentation)
5. Start building features!

---

**Happy coding! 🎉**
