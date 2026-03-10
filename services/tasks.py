import csv
import os
from datetime import datetime

from celery_app import celery
from models import Application, PlacementDrive

EXPORT_FOLDER = "exports"


@celery.task
def export_student_applications(student_id):

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    filename = f"applications_{student_id}.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    with open(filepath, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Application ID",
            "Drive ID",
            "Status",
            "Date"
        ])

        for app_record in applications:
            writer.writerow([
                app_record.id,
                app_record.drive_id,
                app_record.status,
                app_record.applied_on
            ])

    print("CSV generated:", filepath)

    return filepath


@celery.task
def send_deadline_reminders():

    today = datetime.utcnow().date()

    drives = PlacementDrive.query.filter(
        PlacementDrive.application_deadline >= today
    ).all()

    for drive in drives:
        print(f"Reminder: {drive.job_title} deadline approaching")


@celery.task
def monthly_admin_report():

    total_drives = PlacementDrive.query.count()
    total_apps = Application.query.count()

    report = f"""
Monthly Placement Report

Total Drives: {total_drives}
Total Applications: {total_apps}
"""

    print(report)