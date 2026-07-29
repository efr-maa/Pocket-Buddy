"""Budget/summary math — ported from the original expense_tracker.py script.

This is kept separate from the Flask routes on purpose so it can be unit
tested directly (see tests/test_services.py) without needing to spin up a
request. The original CLI script computed "days remaining in the month" and
"remaining budget" from an *all-time* total, which quietly breaks once the
app has been used across more than one month. Here, summaries are always
scoped to a specific year/month so "remaining this month" actually means
this month.
"""

import calendar
from datetime import date
from app.models import Expense


def get_month_summary(user, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    start, end = month_bounds(year, month)
    expenses = (
        Expense.query.filter_by(user_id=user.id)
        .filter(Expense.date_added >= start, Expense.date_added < end)
        .order_by(Expense.date_added.desc())
        .all()
    )

    total_spent = sum(e.amount for e in expenses)

    by_category = {}
    for e in expenses:
        label = e.category.label
        by_category[label] = by_category.get(label, 0) + e.amount

    remaining_budget = user.monthly_budget - total_spent

    days_in_month = calendar.monthrange(year, month)[1]
    if year == today.year and month == today.month:
        remaining_days = max(days_in_month - today.day, 1)
    else:
        # Looking at a past or future month — no "days remaining" concept applies.
        remaining_days = days_in_month

    daily_budget = remaining_budget / remaining_days

    return {
        "year": year,
        "month": month,
        "expenses": expenses,
        "total_spent": total_spent,
        "by_category": by_category,
        "budget": user.monthly_budget,
        "remaining_budget": remaining_budget,
        "daily_budget": daily_budget,
        "remaining_days": remaining_days,
    }


def month_bounds(year, month):
    """Return (start, end) dates spanning the given month, so a range filter
    like `date_added >= start, date_added < end` works identically on
    SQLite and Postgres without relying on either database's own date
    extraction functions.
    """
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    return start, end
