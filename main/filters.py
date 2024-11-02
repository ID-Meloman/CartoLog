# main/filters.py
import django_filters
from .models import Car, Brand

class CarFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = {
            'model__brand__name': ['exact'],  # Здесь добавляем путь через модель Car
        }