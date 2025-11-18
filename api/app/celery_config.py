import os

from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

load_dotenv()

celery = Celery(
    "smaji",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=None,
    include=[
        "app.tasks.scheduled_tasks"
    ]
)

celery.conf.update(
    timezone="Africa/Nairobi",
    enable_utc=False,
)

celery.conf.beat_schedule = {
    "calculate-and-send-yesterday-usage": {
        "task": "app.tasks.scheduled_tasks.calculate_and_send_yesterday_usage",
        "schedule": crontab(hour=1, minute=0),
    }
}
