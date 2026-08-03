# Pocket Buddy

A full-stack rebuild of the original Pocket Buddy CLI expense tracker: real
user accounts, a database, custom categories, a configurable monthly
budget, and a small JSON API behind the dashboard.

## What changed from the original script

- The `Expense` class became a proper database model (`app/models.py`),
  alongside new `User` and `Category` models.
- The terminal prompts (`get_user_expense`) became real web forms.
- Expenses are now tied to a logged-in user and tagged with a date — the
  original script computed "budget left this month" from your *all-time*
  spending, which quietly breaks once you've used it across more than one
  month. Summaries here are always scoped to a specific month
  (`app/services.py`).
- The monthly budget and categories are per-user and editable, instead of
  a hardcoded `$2000` and a fixed 5-item list.
- The pink terminal output (`pink()`) became the site's accent color.

## Project layout

```
pocket-buddy/
  app/
    __init__.py        # app factory, extensions, CLI seed command
    models.py           # User, Category, Expense
    forms.py            # WTForms (register/login/expense/category/budget)
    services.py         # the budget/summary math, unit-testable on its own
    routes/
      auth.py           # register / login / logout
      main.py           # dashboard, expenses CRUD, categories, settings
      api.py            # JSON /api/summary endpoint
    templates/           # Jinja templates (pink-accented CSS)
    static/
  tests/                 # pytest — models, services, and route behavior
  config.py
  wsgi.py                # production entry point (gunicorn)
  requirements.txt
  .env.example
```

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env             # then edit SECRET_KEY if you want
export FLASK_APP=wsgi.py         # set FLASK_APP=wsgi.py on Windows

# optional: seed a demo account (username: demo, password: demo1234)
# with your two original expenses (jsh $93 / Work, Phone plan $30 / Misc)
flask seed-demo

flask run
```

Visit `http://127.0.0.1:5000`. Register your own account, or log in as
`demo` / `demo1234` to see the seeded data.

## Running the tests

```bash
pytest -v
```

13 tests currently cover: default categories on registration, expense/category
relationships, the month-scoped budget math (including a December→January
rollover check), and the main request flows (register, login-required
redirect, add expense, JSON API).

## Deploying (next step, not done yet)

This is set up to deploy cleanly to **Azure App Service** with **Azure
Database for PostgreSQL**, both covered by your Azure for Students credit:

1. Create an Azure Database for PostgreSQL (flexible server, cheapest tier).
2. Create an Azure App Service (Python 3.12 runtime).
3. In the App Service's Configuration, set environment variables:
   - `SECRET_KEY` — a long random string
   - `DATABASE_URL` — your Postgres connection string
   - `FLASK_APP=wsgi.py`
4. Set the startup command to: `gunicorn wsgi:app`
5. Push this repo to GitHub and connect it to the App Service via
   GitHub Actions deployment (Azure sets this up for you from the portal).

We'll walk through this step by step together when you're ready — no need
to do it today.

## Known limitations / good "what's next" talking points

- No password reset flow yet.
- No pagination on the expenses list (fine for personal use, would matter
  at scale).
- The dashboard only shows the current month; the API already accepts
  `?year=&month=` params, so month-switching UI is a natural next feature.
