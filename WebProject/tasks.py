from celery import shared_task
from django.core import management


@shared_task
def clear_and_populate_cars():
    from main.models import CarInShowroom
    CarInShowroom.objects.all().delete()
    print("✅ Таблица CarInShowroom очищена.")

    management.call_command('populate_cars')  # Запуск как manage.py команды
    print("✅ Команда populate_cars выполнена")
    return "Готово!"