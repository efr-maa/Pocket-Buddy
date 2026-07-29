from datetime import date
from app import db
from app.models import Expense, Category
from app.services import get_month_summary, month_bounds


def _add_expense(user, category_name, amount, when):
    cat = Category.query.filter_by(user_id=user.id, name=category_name).first()
    e = Expense(name="test", amount=amount, category_id=cat.id, user_id=user.id, date_added=when)
    db.session.add(e)
    db.session.commit()
    return e


def test_month_bounds_handles_december_rollover():
    start, end = month_bounds(2025, 12)
    assert start == date(2025, 12, 1)
    assert end == date(2026, 1, 1)


def test_summary_only_counts_expenses_in_requested_month(app, user):
    today = date.today()
    _add_expense(user, "Food", 20.0, today)
    _add_expense(user, "Food", 999.0, date(today.year - 1, 1, 15))  # a year-old expense

    summary = get_month_summary(user, today.year, today.month)

    assert summary["total_spent"] == 20.0
    assert summary["by_category"]["🍔 Food"] == 20.0


def test_remaining_budget_and_daily_budget_are_computed_correctly(app, user):
    today = date.today()
    _add_expense(user, "Work", 200.0, today)

    summary = get_month_summary(user, today.year, today.month)

    assert summary["remaining_budget"] == user.monthly_budget - 200.0
    expected_daily = summary["remaining_budget"] / summary["remaining_days"]
    assert round(summary["daily_budget"], 2) == round(expected_daily, 2)


def test_summary_with_no_expenses_is_zeroed_out(app, user):
    today = date.today()
    summary = get_month_summary(user, today.year, today.month)

    assert summary["total_spent"] == 0
    assert summary["by_category"] == {}
    assert summary["remaining_budget"] == user.monthly_budget
