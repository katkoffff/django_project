import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'np.settings')

app = Celery('np')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()