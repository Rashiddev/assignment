from rest_framework import serializers

from car.models import Make, CarModel, CarSubModel


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
