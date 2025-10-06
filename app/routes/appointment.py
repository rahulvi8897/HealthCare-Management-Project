from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Appointment, Patient, Doctor
from .. import db
from flask_login import login_required

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/")
@login_required
def list_appointments():
    appts = Appointment.query.all()
    return render_template("appointments/list.html", appointments=appts)

@appointment_bp.route("/book", methods=["GET", "POST"])
@login_required
def book_appointment():
    if request.method == "POST":
        patient_id = int(request.form["patient_id"])
        doctor_id = int(request.form["doctor_id"])
        date = request.form.get("date")
        time = request.form.get("time")
        a = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time)
        db.session.add(a)
        db.session.commit()
        flash("Appointment requested", "success")
        return redirect(url_for("appointment.list_appointments"))
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template("appointments/book.html", patients=patients, doctors=doctors)
