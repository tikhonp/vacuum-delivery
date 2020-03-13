from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib.auth.models import User


router = routers.DefaultRouter()
router.register('neworders', views.ordersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
