from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import User, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            if not user.is_active:
                return "Account Disabled"
            login_user(user)
            return redirect(f"/{user.role}/dashboard")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


# -------------------------
# STUDENT REGISTER
# -------------------------
@auth_bp.route("/register/student", methods=["GET","POST"])
def register_student():

    if request.method == "POST":

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password_hash=generate_password_hash(request.form["password"]),
            role="student"
        )

        db.session.add(user)
        db.session.commit()

        student = Student(
            user_id=user.id,
            phone=request.form.get("phone"),
            course=request.form.get("course"),
            graduation_year=request.form.get("graduation_year"),
            cgpa=request.form.get("cgpa")  # NEW FIELD
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/login")

    return render_template("register_student.html")


# -------------------------
# COMPANY REGISTER
# -------------------------
@auth_bp.route("/register/company", methods=["GET","POST"])
def register_company():

    if request.method == "POST":

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password_hash=generate_password_hash(request.form["password"]),
            role="company"
        )

        db.session.add(user)
        db.session.commit()

        company = Company(
            user_id=user.id,
            company_name=request.form["company_name"],
            hr_contact=request.form.get("hr_contact"),
            website=request.form.get("website")
        )

        db.session.add(company)
        db.session.commit()

        return redirect("/login")

    return render_template("register_company.html")