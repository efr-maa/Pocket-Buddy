"""Entry point for production servers (gunicorn, Azure App Service, etc.)

Local dev should use `flask run` instead (see README), which picks up
FLASK_APP from .env automatically.
"""

from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
