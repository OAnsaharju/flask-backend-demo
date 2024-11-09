from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes.util_routes import util_bp
from routes.person_routes import person_bp
from routes.user_routes import user_bp
from routes.group_routes import group_bp
from dotenv import load_dotenv
from sqlalchemy import text
from flask_marshmallow import Marshmallow
import os

load_dotenv(dotenv_path="backend/.env")

app = Flask(__name__)

# Database configuration
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

app.config["JWT_SECRET_KEY"] = f"{JWT_SECRET_KEY}"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
jwt = JWTManager(app)


ma = Marshmallow(app)
ma.init_app(app)

app.register_blueprint(person_bp)
app.register_blueprint(user_bp)
app.register_blueprint(group_bp)
app.register_blueprint(util_bp, url_prefix="/utils")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def test_db_connection():
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")


def create_tables():
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            print("All tables created successfully.")
        except Exception as e:
            print(f"Failed to create tables: {e}")


if __name__ == "__main__":
    test_db_connection()
    create_tables()
    app.run(debug=True, host="0.0.0.0")
