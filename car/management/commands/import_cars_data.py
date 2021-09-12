import decimal

from django.core.management.base import BaseCommand

import pandas as pd

from car.models import Make, Car, CarModel, CarSubModel


class Command(BaseCommand):
    help = 'Import Catalog from Excel'

    def handle(self, *args, **options):
        make_df = pd.read_csv("data/makes.csv", error_bad_lines=False)
        row_iter = make_df.iterrows()
        objs = [
            Make(
                name=row['name'],
                slug=row['id'],
                active=True if str.strip(row['active']).lower() == 't' else False,
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ) for index, row in row_iter
        ]
        Make.objects.bulk_create(objs)

        model_df = pd.read_csv("data/models.csv", error_bad_lines=False)
        row_iter = model_df.iterrows()
        objs = []
        for index, row in row_iter:
            make = Make.objects.filter(slug=row['make_id']).first()
            if make:
                objs.append(
                    CarModel(
                        name=row['name'],
                        slug=row['id'],
                        active=True if str.strip(row['active']).lower() == 't' else False,
                        make=make,
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                )
        CarModel.objects.bulk_create(objs)

        submodel_df = pd.read_csv("data/submodels.csv", error_bad_lines=False)
        row_iter = submodel_df.iterrows()
        objs = []
        for index, row in row_iter:
            car_model = CarModel.objects.filter(slug=row['model_id']).first()
            if car_model:
                objs.append(
                    CarSubModel(
                        name=row['name'],
                        slug=row['id'],
                        active=True if str.strip(row['active']).lower() == 't' else False,
                        model=car_model,
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                )
        CarSubModel.objects.bulk_create(objs)

        submodel_df = pd.read_csv("data/cars.csv", error_bad_lines=False)
        row_iter = submodel_df.iterrows()

        for index, row in row_iter:
            make = Make.objects.filter(slug=row['make_id']).first()
            car_model = CarModel.objects.filter(slug=row['model_id']).first()
            car_submodel = CarSubModel.objects.filter(slug=row['submodel_id']).first()
            if all([make, car_model, car_submodel]):
                try:
                    car = Car(
                        hash=row['id'],
                        active=True if str.strip(row['active']).lower() == 't' else False,
                        year=row['year'],
                        mileage=decimal.Decimal(row['mileage']),
                        price=decimal.Decimal(row['price']),
                        make=make,
                        model=car_model,
                        submodel=car_submodel,
                        body_type=row['body_type'],
                        transmission=row['transmission'],
                        fuel_type=row['fuel_type'],
                        exterior_color=row['exterior_color'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                    car.save()
                except Exception as e:
                    pass

        print('Data imported successfully!')



