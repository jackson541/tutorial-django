from django.urls import path
from .views import *


urlpatterns = [
    path('cadastro/', cadastro_leitores, name='cadastro_leitores_view'),
]


