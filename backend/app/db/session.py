from sqlmodel import SQLModel, create_engine, Session
import os

DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))
DB_PATH = os.path.abspath(DB_PATH)
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    SQLModel.metadata.create_all(ENGINE)

def get_session():
    return Session(ENGINE)
