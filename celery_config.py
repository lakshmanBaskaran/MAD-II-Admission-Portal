from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"

timezone = "UTC"
enable_utc = True

beat_schedule = {
    "daily-deadline-reminder": {
        "task": "services.tasks.send_deadline_reminders",
        "schedule": crontab(hour=9, minute=0),
    },

    "monthly-admin-report": {
        "task": "services.tasks.monthly_admin_report",
        "schedule": crontab(day_of_month=1, hour=9, minute=0),
    }
}