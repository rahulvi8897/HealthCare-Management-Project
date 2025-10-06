from flask import Blueprint, render_template, redirect, url_for, request, flash
from .. import db
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    return render_template("index.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form.get("role", "patient")
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash("User already exists - pick another username/email", "warning")
            return redirect(url_for("auth.register"))
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("auth.dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.index"))

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    # redirect to simple role-based dashboard
    return render_template("dashboard.html")
