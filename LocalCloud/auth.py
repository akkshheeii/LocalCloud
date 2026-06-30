from flask import Blueprint, render_template, request, redirect, url_for,flash
from . import db
from .models import User
from flask_login import login_manager, login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:

            if user.password == password:
                login_user(user)
                print(current_user.username)
                flash("Loged In successfully", "Success")
                return redirect(url_for("views.dashboard"))

            else:
                flash("Incorrect Password",'error')
                return render_template('login.html')

        # Register new user
        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()
        flash("Loged In successfully", "success")

        login_user(new_user)
        print(current_user.username)

        return redirect(url_for("views.dashboard"))

    return render_template("login.html")


@auth.route("/logout",methods = ["GET"])
@login_required
def logout():
    if request.method == "POST":
        print("POST")

    logout_user()
    flash("Loged Out succesfully !", "Success")

    return redirect(url_for("auth.login"))