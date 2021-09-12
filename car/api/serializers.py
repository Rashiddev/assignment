from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from car.models import Make, Car, CarModel, CarSubModel


class MakeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ('id', 'name', 'slug', 'active', 'created_at', 'updated_at')


class CarModelListSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.name')

    class Meta:
        model = CarModel
        fields = ('id', 'name', 'active', 'make', 'created_at', 'updated_at')


class CarSubModelListSerializer(serializers.ModelSerializer):
    model = serializers.CharField(source='model.name')

    class Meta:
        model = CarSubModel
        fields = ('id', 'name', 'active', 'model', 'created_at', 'updated_at')


class CarListSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.name')
    model = serializers.CharField(source='model.name')
    submodel = serializers.CharField(source='submodel.name')

    class Meta:
        model = Car
        fields = (
            'id',
            'hash',
            'active',
            'year',
            'mileage',
            'price',
            'make',
            'model',
            'submodel',
            'body_type',
            'transmission',
            'fuel_type',
            'exterior_color',
            'created_at',
            'updated_at'
        )


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'hash',
            'active',
            'year',
            'mileage',
            'price',
            'make',
            'model',
            'submodel',
            'body_type',
            'transmission',
            'fuel_type',
            'exterior_color',
            'created_at',
            'updated_at'
        )

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if not is_valid:
            return is_valid

        make = self.validated_data['make']
        model = self.validated_data['model']
        if not make.carmodel_set.all().filter(id=model.id).exists():
            self._validated_data = {}
            self._errors['message'] = 'Model does not belong to Make!'
            if raise_exception:
                raise ValidationError(self.errors)
            return False

        submodel = self.validated_data['submodel']
        if not model.carsubmodel_set.all().filter(id=submodel.id).exists():
            self._validated_data = {}
            self._errors['message'] = 'Submodel does not belong to Model!'
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        return not bool(self._errors)
