from django.urls import path
from .views import *


urlpatterns = [
    path('primeira_rota/', primeiro_teste, name='primeira_rota_do_app'),
]


