from .celery import app as celery_app
import WebProject.tasks

__all__ = ('celery_app',)