from rest_framework import mixins, viewsets

from car.api import serializers
from car.models import Make, CarModel, CarSubModel


class MakeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Make.objects.all()
    serializer_class = serializers.MakeListSerializer


class CarModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarModel.objects.all()
    serializer_class = serializers.CarModelListSerializer


class CarSubModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarSubModel.objects.all()
    serializer_class = serializers.CarSubModelListSerializer
