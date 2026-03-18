# Quick Start Guide

Get TaskFlow running in 5 minutes! 🚀

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Taskflow.git
cd Taskflow
```

## 2️⃣ Backend Setup (Terminal 1)

```bash
# Activate virtual environment
source venv/bin/activate
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r server/requirements.txt

# Run the backend
python server/app.py
```

✅ Backend running at `http://localhost:5000`

## 3️⃣ Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at `http://localhost:5173`

## 4️⃣ Create a Test Account

Open http://localhost:5173 in your browser and:
1. Click "Register"
2. Fill in username, email, password
3. Click "Register"
4. Login with your credentials

## 5️⃣ Try It Out!

- 📊 **Dashboard**: View task overview
- 📁 **Projects**: Create new projects
- ✅ **Tasks**: Add tasks to projects
- 👥 **Team**: Manage collaborators

## 🎯 Next Steps

- Update `.env.example` to `.env` for custom configuration
- Set up PostgreSQL for production (optional)
- Explore the API at `http://localhost:5000/`
- Check [API Documentation](README.md#-api-documentation) in README

## 📖 Learn More

- [Full README](README.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [API Documentation](README.md#-api-documentation)

---

**Need help?** Check out the [Troubleshooting](README.md#-troubleshooting) section in README.
