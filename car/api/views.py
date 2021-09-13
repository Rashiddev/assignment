from django_filters import rest_framework as d_filters
from rest_framework import filters, mixins, permissions, viewsets

from car.api import serializers, filtersets
from car.models import Make, Car, CarModel, CarSubModel


class MakeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Make.objects.all()
    serializer_class = serializers.MakeListSerializer


class CarModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarModel.objects.all()
    serializer_class = serializers.CarModelListSerializer
    filter_backends = (d_filters.DjangoFilterBackend,)
    filterset_class = filtersets.CarModelFilter


class CarSubModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CarSubModel.objects.all()
    serializer_class = serializers.CarSubModelListSerializer
    filter_backends = (d_filters.DjangoFilterBackend,)
    filterset_class = filtersets.CarSubModelFilter


class CarViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Car.objects.all()
    serializer_class = serializers.CarListSerializer
    filter_backends = (d_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = filtersets.CarFilter
    ordering_fields = ('updated_at', )
    ordering = '-updated_at'

    action_permission_classes = {
        'create': (permissions.IsAuthenticated,),
        'list': (permissions.AllowAny,)
    }
    action_serializers = {
        'create': serializers.CarCreateSerializer,
        'list': serializers.CarListSerializer
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.action_permission_classes[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return super().get_permissions()

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super().get_serializer_class()

