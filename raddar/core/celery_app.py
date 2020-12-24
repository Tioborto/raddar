import asyncio

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from raddar.core.settings import settings
from raddar.db.database import database


@worker_process_init.connect
def startup(**kwargs):
    print("Initializing database connection for worker.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.connect())


@worker_process_shutdown.connect
def shutdown(**kwargs):
    print("Closing database connection for worker.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.disconnect())


celery_app = Celery(
    "raddar",
    broker=settings.QUEUE_URL,
    include=["raddar.lib.managers.detect_secrets_manager"],
)
celery_app.conf.update(task_track_started=True)
