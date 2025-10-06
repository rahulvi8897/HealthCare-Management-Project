from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Patient
from .. import db
from flask_login import login_required, current_user

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/")
@login_required
def list_patients():
    patients = Patient.query.all()
    return render_template("patients/list.html", patients=patients)

@patient_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_patient():
    if request.method == "POST":
        p = Patient(
            name=request.form["name"],
            dob=request.form.get("dob"),
            gender=request.form.get("gender"),
            phone=request.form.get("phone"),
            address=request.form.get("address"),
            medical_history=request.form.get("medical_history")
        )
        db.session.add(p)
        db.session.commit()
        flash("Patient added", "success")
        return redirect(url_for("patient.list_patients"))
    return render_template("patients/add.html")
