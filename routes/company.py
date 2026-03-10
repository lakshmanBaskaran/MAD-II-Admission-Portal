from flask import Blueprint, render_template, request, redirect, send_file
from extensions import db
from models import Company, PlacementDrive, Application, Student, User
from routes.decorators import role_required
from flask_login import current_user
from datetime import datetime
import io

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/dashboard")
@role_required("company")
def dashboard():

    company = Company.query.filter_by(user_id=current_user.id).first()

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    return render_template(
        "company_dashboard.html",
        drives=[d.to_dict() for d in drives]
    )


@company_bp.route("/create_drive", methods=["POST"])
@role_required("company")
def create_drive():

    company = Company.query.filter_by(user_id=current_user.id).first()

    if not company.approved:
        return "Company Not Approved"

    drive = PlacementDrive(
        company_id=company.id,
        job_title=request.form["job_title"],
        job_description=request.form["job_description"],
        eligibility_criteria=request.form.get("eligibility"),
        application_deadline=datetime.strptime(request.form["deadline"], "%Y-%m-%d")
    )

    db.session.add(drive)
    db.session.commit()

    return redirect("/company/dashboard")


@company_bp.route("/applications/<int:drive_id>")
@role_required("company")
def view_applications(drive_id):

    apps = Application.query.filter_by(drive_id=drive_id).all()

    data = []

    for a in apps:

        student = Student.query.get(a.student_id)
        user = User.query.get(student.user_id)

        data.append({
            "id": a.id,
            "student_id": a.student_id,
            "student_name": user.name,
            "status": a.status,
            "cgpa": student.cgpa,
            "resume": student.resume is not None
        })

    return render_template(
        "company_applications.html",
        applications=data
    )


@company_bp.route("/download_resume/<int:student_id>")
@role_required("company")
def download_resume(student_id):

    student = Student.query.get_or_404(student_id)

    if not student.resume:
        return "Resume not found"

    return send_file(
        io.BytesIO(student.resume),
        download_name=student.resume_filename,
        as_attachment=True,
        mimetype="application/pdf"
    )


@company_bp.route("/update_status/<int:app_id>", methods=["POST"])
@role_required("company")
def update_status(app_id):

    app = Application.query.get_or_404(app_id)

    app.status = request.form["status"]

    db.session.commit()

    return redirect("/company/dashboard")