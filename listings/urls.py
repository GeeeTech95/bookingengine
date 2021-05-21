from django.urls import include,path
from rest_framework import routers
from .views import get_available


urlpatterns = [
    path('v1/units/',get_available,name='availabe')
]

