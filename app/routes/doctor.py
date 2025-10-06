from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Doctor
from .. import db
from flask_login import login_required

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route("/")
@login_required
def list_doctors():
    doctors = Doctor.query.all()
    return render_template("doctors/list.html", doctors=doctors)

@doctor_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_doctor():
    if request.method == "POST":
        d = Doctor(
            name=request.form["name"],
            specialization=request.form.get("specialization"),
            phone=request.form.get("phone"),
            email=request.form.get("email")
        )
        db.session.add(d)
        db.session.commit()
        flash("Doctor added", "success")
        return redirect(url_for("doctor.list_doctors"))
    return render_template("doctors/add.html")
