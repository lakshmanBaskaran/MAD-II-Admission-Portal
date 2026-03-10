from celery_app import celery
from app import create_app

flask_app = create_app()


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask

# register tasks
import services.tasks