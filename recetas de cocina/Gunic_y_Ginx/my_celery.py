from my_celery import Celery

celery = Celery(__name__)

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0'
)
