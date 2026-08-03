import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db as _db
from app.models import User, Category


@pytest.fixture
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    """A user with the same default categories a real registration creates."""
    u = User(
        username="tester",
        email="tester@example.com",
        password_hash=generate_password_hash("password123"),
        monthly_budget=2000.0,
    )
    _db.session.add(u)
    _db.session.flush()
    for name, emoji in app.config["DEFAULT_CATEGORIES"]:
        _db.session.add(Category(name=name, emoji=emoji, user_id=u.id))
    _db.session.commit()
    return u


def login(client, username="tester", password="password123"):
    return client.post(
        "/login", data={"username": username, "password": password}, follow_redirects=True
    )
