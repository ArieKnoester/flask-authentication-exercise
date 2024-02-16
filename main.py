# How to generate good secret keys:
# https://flask.palletsprojects.com/en/latest/quickstart/#sessions
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, db
from dotenv import load_dotenv
import os


load_dotenv(".env")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_password = request.form.get("password")
        hashed_password = generate_password_hash(
            password=user_password,
            method="pbkdf2",
            salt_length=8
        )
        # Pycharm Community Edition apparently has a bug which may highlight
        # these arguments as 'unexpected arguments' when using flask_sqlalchemy
        # and any Mixin class.
        new_user = User(
            email=request.form.get("email"),
            password=hashed_password,
            name=request.form.get("name")
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('secrets', name=new_user.name))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_input = request.form.get("email")
        password_input = request.form.get("password")

        # Email has UNIQUE constraint in database table.
        user_exists = db.session.query(db.exists().where(User.email == email_input)).scalar()

        if not user_exists:
            flash("Email not found. Please try again.")
            return render_template("login.html")

        user_to_login = db.session.execute(db.select(User).filter_by(email=email_input)).scalar()
        is_correct_password = check_password_hash(user_to_login.password, password_input)

        if not is_correct_password:
            flash("Password incorrect. Please try again.")
            return render_template("login.html")

        login_user(user_to_login)
        return redirect(url_for('secrets'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        directory="static",
        path="files/cheat_sheet.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
