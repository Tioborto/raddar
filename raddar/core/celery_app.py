from celery import Celery

celery_app = Celery(
    "raddar",
    broker="pyamqp://guest@queue//",
    include=["raddar.lib.managers.detect_secrets_manager"],
)
celery_app.conf.update(task_track_started=True)
