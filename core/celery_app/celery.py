"""
Celery configuration for core project.
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'fetch-live-matches-every-30-sec': {
        'task': 'matches.tasks.fetch_live_matches',
        'schedule': 30.0,
        'options': {'queue': 'live'},
    },
    'update-standings-every-5-min': {
        'task': 'standings.tasks.update_all_standings',
        'schedule': crontab(minute='*/5'),
        'options': {'queue': 'default'},
    },
    'sync-external-data-every-hour': {
        'task': 'matches.tasks.sync_external_fixtures',
        'schedule': crontab(minute=0, hour='*/1'),
        'options': {'queue': 'default'},
    },
    'cleanup-old-notifications-daily': {
        'task': 'notifications.tasks.cleanup_old_notifications',
        'schedule': crontab(minute=0, hour=2),
        'options': {'queue': 'default'},
    },
    'update-poll-caches-every-10-sec': {
        'task': 'polls.tasks.update_poll_caches',
        'schedule': 10.0,
        'options': {'queue': 'live'},
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')