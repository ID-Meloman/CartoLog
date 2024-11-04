from django_filters import rest_framework as filters
from .models import Car

class CarFilter(filters.FilterSet):
    drive_type = filters.CharFilter(field_name="configuration__transmission_drive__drive_type", lookup_expr="iexact")
    transmission = filters.CharFilter(field_name="configuration__transmission_drive__transmission", lookup_expr="iexact")
    horsepower_min = filters.NumberFilter(field_name="configuration__technical_specs__horsepower", lookup_expr="gte")
    horsepower_max = filters.NumberFilter(field_name="configuration__technical_specs__horsepower", lookup_expr="lte")

    class Meta:
        model = Car
        fields = ['drive_type', 'transmission', 'horsepower_min', 'horsepower_max']