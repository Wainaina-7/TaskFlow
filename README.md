# TaskFlow

TaskFlow is a full-stack task and project management app built with **Flask (Python)**, **React (Vite)**, and **PostgreSQL**.

It demonstrates:
- A structured data model with **Users**, **Projects**, **Tasks**, and **Collaborations**
- A **Flask API** (CRUD endpoints) powered by **Flask-SQLAlchemy**
- A modern **React frontend** using **React Router**, **Formik**, and **Yup**
- Full **frontend/backend integration** using `fetch()`

---

## Features

- Create, edit, and delete **tasks**
- Create **projects**
- Add collaborators to projects with roles (Manager / Developer / Viewer)
- Track task status and assignment

---

## Getting Started

### Backend (Flask)

1. Activate the Python virtual environment:
   ```bash
   cd TaskFlow
   source venv/bin/activate
   ```

2. Ensure PostgreSQL is running and create the DB:
   ```bash
   sudo -u postgres createdb taskflow_db
   ```

   If you want to use a dedicated user/password (recommended):
   ```bash
   sudo -u postgres createuser taskflow_user
   sudo -u postgres psql -c "ALTER USER taskflow_user WITH PASSWORD 'secret';"
   sudo -u postgres createdb -O taskflow_user taskflow_db
   ```

3. Point the backend to Postgres (preferred) by exporting a `DATABASE_URL`:
   ```bash
   export DATABASE_URL="postgresql://taskflow_user:secret@localhost:5432/taskflow_db"
   ```

   > If you don't set `DATABASE_URL`, TaskFlow will still work using a local SQLite file (`taskflow.db`).

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
