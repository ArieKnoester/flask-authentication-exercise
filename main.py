import dotenv
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from models.user import User, db
from dotenv import load_dotenv
import os


load_dotenv(".env")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form.get("name"))
        new_user = User(
            email=request.form.get("email"),
            password=request.form.get("password"),
            name=request.form.get("name")
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('secrets', name=new_user.name))

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    user_name = request.args.get("name")
    return render_template("secrets.html", user_name=user_name)


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    pass


if __name__ == "__main__":
    app.run(debug=True)
