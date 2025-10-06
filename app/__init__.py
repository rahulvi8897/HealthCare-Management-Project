from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.patient import patient_bp
    from .routes.doctor import doctor_bp
    from .routes.appointment import appointment_bp
    from .models import User, Patient, Doctor, Appointment, Prescription, Billing

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp, url_prefix="/patients")
    app.register_blueprint(doctor_bp, url_prefix="/doctors")
    app.register_blueprint(appointment_bp, url_prefix="/appointments")

    with app.app_context():
        db.create_all()

    return app
