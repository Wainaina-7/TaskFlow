class Config: 
    # Use password auth for Postgres (set by `ALTER USER postgres WITH PASSWORD 'password'`)
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/taskflow_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False