import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'np.settings')

app = Celery('np')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_news_every_monday': {
    'task': 'news.tasks.send_weekly_news',
    'schedule': crontab(hour=8, minute=0,day_of_week='monday'),
    #'schedule': crontab(),
    'args': (),
    },
}