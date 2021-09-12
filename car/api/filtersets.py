from django_filters import rest_framework as filters

from car.models import Car


class CarFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='lte')

    class Meta:
        model = Car
        fields = (
            'min_price',
            'max_price',
            'min_mileage',
            'max_mileage'
        )
