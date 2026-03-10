from app import app
from extensions import db
from models import User, Student, Company, PlacementDrive, Application
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
import random

with app.app_context():

    print("Clearing old data...")

    Application.query.delete()
    PlacementDrive.query.delete()
    Student.query.delete()
    Company.query.delete()
    User.query.delete()

    db.session.commit()

    # -----------------------
    # USERS
    # -----------------------

    print("Creating users...")

    student_users = []
    company_users = []

    for i in range(1, 41):
        u = User(
            name=f"Student {i}",
            email=f"student{i}@portal.com",
            password_hash=generate_password_hash("password"),
            role="student"
        )
        db.session.add(u)
        student_users.append(u)

    for i in range(1, 11):
        u = User(
            name=f"HR {i}",
            email=f"company{i}@portal.com",
            password_hash=generate_password_hash("password"),
            role="company"
        )
        db.session.add(u)
        company_users.append(u)

    admin = User(
        name="Admin",
        email="admin@portal.com",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    # -----------------------
    # STUDENTS
    # -----------------------

    print("Creating student profiles...")

    students = []

    for user in student_users:

        cgpa = round(random.uniform(5.5, 9.5), 2)

        student = Student(
            user_id=user.id,
            phone="9876543210",
            course=random.choice([
                "B.Tech CSE",
                "B.Tech IT",
                "B.Tech ECE",
                "B.Tech AI"
            ]),
            graduation_year=random.choice([2024, 2025, 2026]),
            cgpa=cgpa
        )

        db.session.add(student)
        students.append(student)

    db.session.commit()

    # -----------------------
    # COMPANIES
    # -----------------------

    print("Creating companies...")

    companies = []

    company_names = [
        "Google", "Amazon", "Microsoft", "Meta",
        "Intel", "IBM", "Oracle", "Adobe",
        "Salesforce", "Nvidia"
    ]

    for i, user in enumerate(company_users):

        company = Company(
            user_id=user.id,
            company_name=company_names[i],
            hr_contact="9876543210",
            website="https://company.com",
            approved=True
        )

        db.session.add(company)
        companies.append(company)

    db.session.commit()

    # -----------------------
    # PLACEMENT DRIVES
    # -----------------------

    print("Creating placement drives...")

    drives = []

    jobs = [
        "Software Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Cloud Engineer",
        "DevOps Engineer"
    ]

    for i in range(25):

        company = random.choice(companies)

        min_cgpa = round(random.uniform(6.0, 8.5), 1)

        drive = PlacementDrive(
            company_id=company.id,
            job_title=random.choice(jobs),
            job_description="Exciting role for talented engineers",
            eligibility_criteria=str(min_cgpa),
            application_deadline=date.today() + timedelta(days=random.randint(20, 90)),
            status="Approved"
        )

        db.session.add(drive)
        drives.append(drive)

    db.session.commit()

    # -----------------------
    # APPLICATIONS
    # -----------------------

    print("Creating applications...")

    for student in students:

        applied_drives = random.sample(drives, k=random.randint(4, 10))

        for drive in applied_drives:

            try:

                application = Application(
                    student_id=student.id,
                    drive_id=drive.id,
                    status=random.choice([
                        "Applied",
                        "Shortlisted",
                        "Rejected",
                        "Selected"
                    ]),
                    applied_on=datetime.utcnow()
                )

                db.session.add(application)

            except:
                pass

    db.session.commit()

    print("Level 2 database seeded successfully!")