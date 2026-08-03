from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import Expense, Category
from app.forms import ExpenseForm, CategoryForm, BudgetForm
from app.services import get_month_summary

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    today = date.today()
    summary = get_month_summary(current_user, today.year, today.month)
    return render_template("dashboard.html", summary=summary, today=today)


@main_bp.route("/expenses")
@login_required
def expenses_list():
    expenses = (
        Expense.query.filter_by(user_id=current_user.id)
        .order_by(Expense.date_added.desc())
        .all()
    )
    return render_template("expenses.html", expenses=expenses)


def _populate_category_choices(form):
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    form.category_id.choices = [(c.id, c.label) for c in categories]
    return categories


@main_bp.route("/expenses/add", methods=["GET", "POST"])
@login_required
def add_expense():
    form = ExpenseForm()
    categories = _populate_category_choices(form)

    if not categories:
        flash("Add a category first before logging an expense.", "info")
        return redirect(url_for("main.manage_categories"))

    if form.validate_on_submit():
        expense = Expense(
            name=form.name.data,
            amount=form.amount.data,
            category_id=form.category_id.data,
            date_added=form.date_added.data,
            user_id=current_user.id,
        )
        db.session.add(expense)
        db.session.commit()
        flash(f"Added {expense.name} (${expense.amount:.2f}).", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("add_expense.html", form=form)


@main_bp.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    form = ExpenseForm(obj=expense)
    _populate_category_choices(form)

    if form.validate_on_submit():
        expense.name = form.name.data
        expense.amount = form.amount.data
        expense.category_id = form.category_id.data
        expense.date_added = form.date_added.data
        db.session.commit()
        flash("Expense updated.", "success")
        return redirect(url_for("main.expenses_list"))

    return render_template("add_expense.html", form=form, editing=True)


@main_bp.route("/expenses/<int:expense_id>/delete", methods=["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted.", "info")
    return redirect(url_for("main.expenses_list"))


@main_bp.route("/categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    form = CategoryForm()
    if form.validate_on_submit():
        exists = Category.query.filter_by(user_id=current_user.id, name=form.name.data).first()
        if exists:
            flash("You already have a category with that name.", "danger")
        else:
            category = Category(
                name=form.name.data,
                emoji=form.emoji.data or "✨",
                user_id=current_user.id,
            )
            db.session.add(category)
            db.session.commit()
            flash(f"Added category {category.label}.", "success")
        return redirect(url_for("main.manage_categories"))

    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    return render_template("categories.html", form=form, categories=categories)


@main_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    if category.expenses:
        flash("Can't delete a category that already has expenses tied to it.", "danger")
    else:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted.", "info")
    return redirect(url_for("main.manage_categories"))


@main_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = BudgetForm(monthly_budget=current_user.monthly_budget)
    if form.validate_on_submit():
        current_user.monthly_budget = form.monthly_budget.data
        db.session.commit()
        flash("Budget updated.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("settings.html", form=form)
