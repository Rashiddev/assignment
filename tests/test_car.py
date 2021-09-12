from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from car import factories
from car.models import Make, Car, CarModel, CarSubModel


class Tests(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(username='rashid', email='rashiidmahmood@gmail.com')
        self.user.set_password('password')
        self.user.save()
        # self.make = Make.objects.create()

    def force_login(self):
        self.client.force_login(user=self.user)

    def test_make_list_view(self):
        response = self.client.get(reverse('car_api:make-list'))
        self.assertEqual(
            response.data["count"], 0
        )

        make_1 = factories.MakeFactory(name='Nissan')
        factories.MakeFactory()
        factories.MakeFactory()

        response = self.client.get(reverse('car_api:make-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"], Make.objects.count()
        )
        self.assertContains(response, make_1.name)

    def test_model_list_view(self):
        response = self.client.get(reverse('car_api:carmodel-list'))
        self.assertEqual(
            response.data["count"], 0
        )

        model_1 = factories.CarModelFactory(name='Path Finder')
        factories.CarModelFactory()

        response = self.client.get(reverse('car_api:carmodel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"], CarModel.objects.count()
        )
        self.assertContains(response, model_1.name)
        self.assertContains(response, model_1.make.name)

    def test_submodel_list_view(self):
        response = self.client.get(reverse('car_api:carsubmodel-list'))
        self.assertEqual(
            response.data["count"], 0
        )

        make = factories.MakeFactory(name='Nissan')
        model = factories.CarModelFactory(name='Path Finder', make=make)
        submodel_1 = factories.CarSubModelFactory(name='2013', model=model)
        submodel_2 = factories.CarSubModelFactory(name='2015', model=model)
        submodel_3 = factories.CarSubModelFactory(name='2018', model=model)
        submodel_4 = factories.CarSubModelFactory(name='2021', model=model)

        self.assertEqual(submodel_1.model, model)
        self.assertEqual(submodel_1.model.make, make)
        self.assertEqual(submodel_2.model, model)
        self.assertEqual(submodel_2.model.make, make)

        response = self.client.get(reverse('car_api:carsubmodel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"], CarSubModel.objects.count()
        )
        self.assertNotContains(response, make.name)
        self.assertContains(response, model.name)
        self.assertContains(response, submodel_3.name)
        self.assertContains(response, submodel_4.name)

    def test_car_list_view(self):
        response = self.client.get(reverse('car_api:car-list'))
        self.assertEqual(
            response.data["count"], 0
        )

        car1 = factories.CarFactory()
        car2 = factories.CarFactory()
        car3 = factories.CarFactory()

        response = self.client.get(reverse('car_api:car-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"], Car.objects.count()
        )
        self.assertContains(response, car2.make.name)
        self.assertContains(response, car1.model.name)
        self.assertContains(response, car3.submodel.name)

    def test_car_list_view_with_mileage_filter(self):
        response = self.client.get(reverse('car_api:car-list'))
        self.assertEqual(
            response.data["count"], 0
        )

        car1 = factories.CarFactory(mileage=150000)
        car2 = factories.CarFactory(mileage=110000)
        car3 = factories.CarFactory(mileage=70000)
        car4 = factories.CarFactory(mileage=30000)
        car5 = factories.CarFactory(mileage=200000)

        response = self.client.get(f"{reverse('car_api:car-list')}?min_mileage=30000&max_mileage=120000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"], 3
        )
        self.assertContains(response, car2.mileage)
        self.assertNotContains(response, car1.mileage)
        self.assertNotContains(response, car5.mileage)

    def test_car_list_view_with_price_filter(self):
        response = self.client.get(reverse('car_api:car-list'))
        self.assertEqual(
            response.data["count"], 0
        )

        car1 = factories.CarFactory(price=15000)
        car2 = factories.CarFactory(price=25000)
        car3 = factories.CarFactory(price=50000)
        car4 = factories.CarFactory(price=100000)
        car5 = factories.CarFactory(price=200000)

        response = self.client.get(f"{reverse('car_api:car-list')}?min_price=100000&max_price=300000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"], 2
        )
        self.assertContains(response, car5.mileage)
        self.assertContains(response, car4.mileage)
        self.assertNotContains(response, car1.mileage)

    def test_create_new_car(self):
        self.force_login()

        make = factories.MakeFactory()
        model = factories.CarModelFactory(make=make)
        submodel = factories.CarSubModelFactory(model=model)

        data = {
            'year': '2018',
            'mileage': '200000',
            'price': '45000',
            'make': make.id,
            'model': model.id,
            'submodel': submodel.id,
            'transmission': Car.TRANSMISSION.manual,
            'fuel_type': Car.FUEL_TYPE.petrol,
            'exterior_color': 'Grey'
        }

        response = self.client.post(reverse('car_api:car-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertTrue(Car.objects.filter(
            make=make.id, model=model.id, submodel=submodel.id, exterior_color='Grey'
        ).exists())

    def test_create_new_car_should_not_work_without_authentication(self):
        make = factories.MakeFactory()
        model = factories.CarModelFactory(make=make)
        submodel = factories.CarSubModelFactory(model=model)

        data = {
            'year': '2018',
            'mileage': '200000',
            'price': '45000',
            'make': make.id,
            'model': model.id,
            'submodel': submodel.id,
            'transmission': Car.TRANSMISSION.manual,
            'fuel_type': Car.FUEL_TYPE.petrol,
            'exterior_color': 'Grey'
        }

        response = self.client.post(reverse('car_api:car-list'), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_car_should_fail_if_model_not_in_make(self):
        self.force_login()

        make = factories.MakeFactory(name='Nissan')
        model = factories.CarModelFactory(name='X6', make=factories.MakeFactory(name='BMW'))
        submodel = factories.CarSubModelFactory(model=model)

        data = {
            'year': '2018',
            'mileage': '200000',
            'price': '45000',
            'make': make.id,
            'model': model.id,
            'submodel': submodel.id,
            'transmission': Car.TRANSMISSION.manual,
            'fuel_type': Car.FUEL_TYPE.petrol,
            'exterior_color': 'Grey'
        }

        response = self.client.post(reverse('car_api:car-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(
            response, 'Model does not belong to Make!',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_create_new_car_should_fail_if_submodel_not_in_model(self):
        self.force_login()

        make = factories.MakeFactory(name='Nissan')
        model = factories.CarModelFactory(name='Path Finder', make=make)
        submodel = factories.CarSubModelFactory(
            model=factories.CarModelFactory(name='X6', make=factories.MakeFactory(name='BMW'))
        )

        data = {
            'year': '2018',
            'mileage': '200000',
            'price': '45000',
            'make': make.id,
            'model': model.id,
            'submodel': submodel.id,
            'transmission': Car.TRANSMISSION.manual,
            'fuel_type': Car.FUEL_TYPE.petrol,
            'exterior_color': 'Grey'
        }

        response = self.client.post(reverse('car_api:car-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(
            response, 'Submodel does not belong to Model!',
            status_code=status.HTTP_400_BAD_REQUEST
        )