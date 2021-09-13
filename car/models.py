from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from model_utils import Choices

from .services import generate_hash


class Make(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class CarModel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('name', 'make')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.make.name}-{self.name}'


class CarSubModel(models.Model):
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    model = models.ForeignKey(CarModel, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Car(models.Model):
    TRANSMISSION = Choices('automatic', 'manual')
    FUEL_TYPE = Choices('diesel', 'electricity', 'hybrid', 'petrol')

    hash = models.CharField(max_length=100, default=generate_hash, unique=True)
    active = models.BooleanField(default=True)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1886),])
    mileage = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField()
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    submodel = models.ForeignKey(CarSubModel, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=100, blank=True)
    transmission = models.CharField(choices=TRANSMISSION, default=TRANSMISSION.automatic, max_length=9)
    fuel_type = models.CharField(choices=FUEL_TYPE, max_length=11)
    exterior_color = models.CharField(max_length=50)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.model}'


