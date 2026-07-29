"""A small JSON API layer over the same summary logic used by the dashboard
page. This is what lets the dashboard refresh its numbers via fetch()
without a full page reload when the user switches months, and it's a
reusable endpoint independent of any particular template.
"""

from datetime import date
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.services import get_month_summary

api_bp = Blueprint("api", __name__)


@api_bp.route("/summary")
@login_required
def summary():
    today = date.today()
    year = request.args.get("year", type=int, default=today.year)
    month = request.args.get("month", type=int, default=today.month)

    if month < 1 or month > 12:
        return jsonify({"error": "month must be between 1 and 12"}), 400

    data = get_month_summary(current_user, year, month)

    return jsonify(
        {
            "year": data["year"],
            "month": data["month"],
            "total_spent": round(data["total_spent"], 2),
            "budget": round(data["budget"], 2),
            "remaining_budget": round(data["remaining_budget"], 2),
            "daily_budget": round(data["daily_budget"], 2),
            "by_category": {k: round(v, 2) for k, v in data["by_category"].items()},
            "expense_count": len(data["expenses"]),
        }
    )
