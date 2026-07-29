import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config shared by all environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    
    _database_url = os.environ.get("DATABASE_URL")
    if _database_url and _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _database_url or "sqlite:///" + os.path.join(
        basedir, "instance", "pocketbuddy.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    DEFAULT_CATEGORIES = [
        ("Food", "🍔"),
        ("Home", "🏠"),
        ("Work", "💼"),
        ("Fun", "🎉"),
        ("Misc", "✨"),
    ]

    DEFAULT_MONTHLY_BUDGET = 2000.0


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
