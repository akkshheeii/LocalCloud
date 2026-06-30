from flask import Flask, render_template, url_for
from flask_login import LoginManager, UserMixin, current_user, login_manager,logout_user,user_unauthorized
from flask_sqlalchemy import SQLAlchemy
import os

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)




db = SQLAlchemy()

from LocalCloud import models
from .models import User,File
from .auth import auth
from .views import views

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "aSBB"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.register_blueprint(auth)
    app.register_blueprint(views)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    @app.route("/",methods=["GET"])
    def home():
        if user_unauthorized:
            print("Unautherized")
            return render_template("login.html")
        return render_template("index.html")

    @app.errorhandler(404)
    def error():
        return render_template("404.html")

    return app

