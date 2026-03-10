from flask import Blueprint, render_template, redirect, request, Response, send_file
from extensions import db
from models import PlacementDrive, Application, Student
from routes.decorators import role_required
from flask_login import current_user
import csv
import io

student_bp = Blueprint("student", __name__, url_prefix="/student")


# ---------------------------
# STUDENT DASHBOARD
# ---------------------------
@student_bp.route("/dashboard")
@role_required("student")
def dashboard():

    drives = PlacementDrive.query.filter_by(status="Approved").all()

    return render_template(
        "student_dashboard.html",
        drives=[d.to_dict() for d in drives]
    )


# ---------------------------
# APPLY WITH CGPA ELIGIBILITY CHECK
# ---------------------------
@student_bp.route("/apply/<int:drive_id>")
@role_required("student")
def apply(drive_id):

    student = Student.query.filter_by(user_id=current_user.id).first()

    if not student:
        return "Student profile not found."

    drive = PlacementDrive.query.get_or_404(drive_id)

    # CGPA eligibility validation
    if drive.eligibility_criteria:

        try:
            required_cgpa = float(drive.eligibility_criteria)

            if student.cgpa is None:
                return "Your CGPA is not set."

            if student.cgpa < required_cgpa:
                return "You are not eligible for this drive."

        except ValueError:
            pass

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if not existing:

        app = Application(
            student_id=student.id,
            drive_id=drive_id
        )

        db.session.add(app)
        db.session.commit()

    return redirect("/student/dashboard")


# ---------------------------
# APPLICATION HISTORY
# ---------------------------
@student_bp.route("/applications")
@role_required("student")
def view_applications():

    student = Student.query.filter_by(user_id=current_user.id).first()

    if not student:
        return "Student profile not found."

    apps = Application.query.filter_by(student_id=student.id).all()

    return render_template(
        "student_applications.html",
        applications=[a.to_dict() for a in apps]
    )


# ---------------------------
# EXPORT CSV
# ---------------------------
@student_bp.route("/export")
@role_required("student")
def export_csv():

    student = Student.query.filter_by(user_id=current_user.id).first()

    if not student:
        return "Student profile not found."

    applications = Application.query.filter_by(student_id=student.id).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Application ID",
        "Drive ID",
        "Status",
        "Applied On"
    ])

    for app in applications:
        writer.writerow([
            app.id,
            app.drive_id,
            app.status,
            app.applied_on
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename=applications_{student.id}.csv"
        }
    )


# ---------------------------
# STUDENT PROFILE PAGE
# ---------------------------
@student_bp.route("/profile")
@role_required("student")
def profile():

    student = Student.query.filter_by(user_id=current_user.id).first()

    return render_template(
        "student_profile.html",
        student=student
    )


# ---------------------------
# UPDATE PROFILE
# ---------------------------
@student_bp.route("/update_profile", methods=["POST"])
@role_required("student")
def update_profile():

    student = Student.query.filter_by(user_id=current_user.id).first()

    student.phone = request.form.get("phone")
    student.course = request.form.get("course")
    student.graduation_year = request.form.get("graduation_year")

    db.session.commit()

    return redirect("/student/profile")


# ---------------------------
# RESUME UPLOAD (STORE IN DB)
# ---------------------------
@student_bp.route("/upload_resume", methods=["POST"])
@role_required("student")
def upload_resume():

    student = Student.query.filter_by(user_id=current_user.id).first()

    file = request.files.get("resume")

    if file:

        student.resume = file.read()            # store file binary
        student.resume_filename = file.filename

        db.session.commit()

    return redirect("/student/profile")


# ---------------------------
# DOWNLOAD RESUME
# ---------------------------
@student_bp.route("/download_resume/<int:student_id>")
@role_required("student")
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