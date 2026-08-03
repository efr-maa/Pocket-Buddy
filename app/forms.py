from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from datetime import date


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password")]
    )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class ExpenseForm(FlaskForm):
    name = StringField("Expense name", validators=[DataRequired(), Length(max=120)])
    amount = FloatField("Amount ($)", validators=[DataRequired(), NumberRange(min=0.01)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    date_added = DateField("Date", default=date.today, validators=[DataRequired()])


class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired(), Length(max=50)])
    emoji = StringField("Emoji (optional)", validators=[Length(max=8)])


class BudgetForm(FlaskForm):
    monthly_budget = FloatField(
        "Monthly budget ($)", validators=[DataRequired(), NumberRange(min=0)]
    )
