from app.celery_config import celery


@celery.task(name='app.tasks.scheduled_tasks.calculate_and_send_yesterday_usage')
def calculate_and_send_yesterday_usage() -> None:
    # TODO: Calculate yesterday's usage for every user and notify them
    print("Yesterday usage calculated and notified.")
    pass
