from django.urls import path, include
from rest_framework import routers

from car.api import views

app_name = "car_api"

router = routers.DefaultRouter()
router.register(r"makes", views.MakeViewSet)
router.register(r"models", views.CarModelViewSet)
router.register(r"submodels", views.CarSubModelViewSet)
router.register(r"cars", views.CarViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
