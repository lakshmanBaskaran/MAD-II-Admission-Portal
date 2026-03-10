from extensions import db
from flask_login import UserMixin
from datetime import datetime


# -----------------------
# USER MODEL
# -----------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": str(self.created_at)
        }


# -----------------------
# STUDENT MODEL
# -----------------------
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    phone = db.Column(db.String(20))
    course = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)

    # STORE RESUME IN DATABASE
    resume = db.Column(db.LargeBinary)
    resume_filename = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "phone": self.phone,
            "course": self.course,
            "graduation_year": self.graduation_year,
            "cgpa": self.cgpa,
            "resume_filename": self.resume_filename
        }


# -----------------------
# COMPANY MODEL
# -----------------------
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(150))

    approved = db.Column(db.Boolean, default=False)
    blacklisted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "approved": self.approved,
            "blacklisted": self.blacklisted
        }


# -----------------------
# PLACEMENT DRIVE MODEL
# -----------------------
class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.String(200))
    application_deadline = db.Column(db.Date)

    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "eligibility_criteria": self.eligibility_criteria,
            "application_deadline": str(self.application_deadline),
            "status": self.status,
            "created_at": str(self.created_at)
        }


# -----------------------
# APPLICATION MODEL
# -----------------------
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)

    status = db.Column(db.String(30), default="Applied")
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "drive_id": self.drive_id,
            "status": self.status,
            "applied_on": str(self.applied_on)
        }