import os
from celery import Celery
from celery.schedules import crontab

broker = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")

app = Celery(
    "eleo_worker",
    broker=broker,
    include=["worker.tasks"],
)

# rebuild the knowledge base every day at 2 AM
app.conf.beat_schedule = {
    "rebuild-index-daily": {
        "task": "worker.tasks.rebuild_index",
        "schedule": crontab(hour=2, minute=0),
    }
}

app.conf.timezone = "Asia/Kolkata"
