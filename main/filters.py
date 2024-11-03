import django_filters
from .models import Car, Brand, CarModel

class CarFilter(django_filters.FilterSet):
    model = django_filters.ModelChoiceFilter(queryset=CarModel.objects.all(), label='Модель')

    class Meta:
        model = Car
        fields = {
            'model__brand__name': ['exact'],  # Фильтрация по марке
            'model': ['exact'],  # Фильтрация по модели
        }
