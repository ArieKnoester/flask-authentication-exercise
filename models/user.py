from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
# UserMixin provides the default properties and methods needed for authentication:
# https://flask-login.readthedocs.io/en/latest/#your-user-class
from flask_login import UserMixin


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
