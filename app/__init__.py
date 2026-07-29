import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(config_object="config.Config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    register_cli(app)

    with app.app_context():
        db.create_all()

    return app


def register_cli(app):
    @app.cli.command("seed-demo")
    def seed_demo():
        """Create a demo user with default categories and the two sample
        expenses that were originally in expenses.csv, so the app isn't
        empty on first run."""
        from app.models import User, Category, Expense
        from werkzeug.security import generate_password_hash
        from datetime import date

        username = "demo"
        existing = User.query.filter_by(username=username).first()
        if existing:
            print("Demo user already exists — skipping seed.")
            return

        user = User(
            username=username,
            email="demo@pocketbuddy.local",
            password_hash=generate_password_hash("demo1234"),
            monthly_budget=app.config["DEFAULT_MONTHLY_BUDGET"],
        )
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        categories = {}
        for name, emoji in app.config["DEFAULT_CATEGORIES"]:
            cat = Category(name=name, emoji=emoji, user_id=user.id)
            db.session.add(cat)
            db.session.flush()
            categories[name] = cat

        # These two match the real entries from the original expenses.csv.
        # The original CSV never recorded a date, so both are seeded as
        # today's date — edit them after seeding if you want accurate dates.
        db.session.add(
            Expense(
                name="jsh",
                amount=93.0,
                category_id=categories["Work"].id,
                user_id=user.id,
                date_added=date.today(),
            )
        )
        db.session.add(
            Expense(
                name="Phone plan",
                amount=30.0,
                category_id=categories["Misc"].id,
                user_id=user.id,
                date_added=date.today(),
            )
        )
        db.session.commit()
        print(f"Seeded demo user (username: {username}, password: demo1234) with 2 sample expenses.")
