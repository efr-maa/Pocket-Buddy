from app.models import Category
from tests.conftest import login


def test_register_creates_user_with_default_categories(client, app):
    resp = client.post(
        "/register",
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Dashboard" in resp.data or b"dashboard" in resp.data.lower() or resp.request.path == "/dashboard"

    from app.models import User

    u = User.query.filter_by(username="newuser").first()
    assert u is not None
    assert Category.query.filter_by(user_id=u.id).count() == 5


def test_login_required_redirects_to_login(client):
    resp = client.get("/dashboard", follow_redirects=True)
    assert b"Log in" in resp.data


def test_dashboard_loads_after_login(client, user):
    login(client)
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert b"Hey, tester" in resp.data


def test_add_expense_flow(client, user):
    login(client)
    cat = Category.query.filter_by(user_id=user.id, name="Food").first()

    resp = client.post(
        "/expenses/add",
        data={
            "name": "Groceries",
            "amount": "45.50",
            "category_id": str(cat.id),
            "date_added": "2026-07-28",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    resp = client.get("/expenses")
    assert b"Groceries" in resp.data


def test_api_summary_requires_login(client):
    resp = client.get("/api/summary")
    assert resp.status_code in (302, 401)


def test_api_summary_returns_json(client, user):
    login(client)
    resp = client.get("/api/summary")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total_spent" in data
    assert "by_category" in data
