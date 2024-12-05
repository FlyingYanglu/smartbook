from celery import Celery


def create_celery(app=None):
    """Create and configure Celery instance."""
    celery = Celery(app.import_name)
    if app:
        celery.conf.update(app.config)
    return celery
