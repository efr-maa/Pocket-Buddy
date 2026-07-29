from datetime import date
from app import db
from app.models import Expense, Category


def test_category_label_combines_emoji_and_name(app, user):
    cat = Category.query.filter_by(user_id=user.id, name="Food").first()
    assert cat.label == "🍔 Food"


def test_expense_belongs_to_user_and_category(app, user):
    cat = Category.query.filter_by(user_id=user.id, name="Work").first()
    expense = Expense(
        name="jsh", amount=93.0, category_id=cat.id, user_id=user.id, date_added=date.today()
    )
    db.session.add(expense)
    db.session.commit()

    assert expense in user.expenses
    assert expense.category.name == "Work"


def test_category_name_unique_per_user(app, user):
    dup = Category(name="Food", emoji="🍕", user_id=user.id)
    db.session.add(dup)
    try:
        db.session.commit()
        assert False, "expected a uniqueness violation"
    except Exception:
        db.session.rollback()
