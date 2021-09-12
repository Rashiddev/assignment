from django.utils.text import slugify

import factory


class MakeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'car.Make'
        django_get_or_create = ('slug',)

    name = factory.sequence(lambda n: f'make {n}')
    slug = factory.LazyAttribute(lambda o: f'{slugify(o.name)}')


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'car.CarModel'
        django_get_or_create = ('name', 'make')

    name = factory.sequence(lambda n: f'model {n}')
    make = factory.SubFactory(MakeFactory)


class CarSubModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'car.CarSubModel'

    name = factory.sequence(lambda n: f'submodel {n}')
    model = factory.SubFactory(CarModelFactory)


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'car.Car'

    hash = factory.sequence(lambda n: n)
    mileage = factory.sequence(lambda n: n)
    price = factory.sequence(lambda n: n)
    year = factory.sequence(lambda n: n + 1900)
    make = factory.SubFactory(MakeFactory)
    model = factory.SubFactory(CarModelFactory)
    submodel = factory.SubFactory(CarSubModelFactory)
