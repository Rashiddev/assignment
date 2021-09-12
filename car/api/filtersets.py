from django_filters import rest_framework as filters

from car.models import Car


class CarFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    max_mileage = filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    make = filters.CharFilter(field_name='make__name', lookup_expr='iexact')
    model = filters.CharFilter(field_name='model__name', lookup_expr='iexact')
    submodel = filters.CharFilter(field_name='submodel__name', lookup_expr='iexact')

    class Meta:
        model = Car
        fields = (
            'min_price',
            'max_price',
            'min_mileage',
            'max_mileage',
            'make',
            'model',
            'submodel'
        )
