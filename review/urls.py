from django.urls import path
from django.views.generic.base import TemplateView
from .views import *

app_name = 'ulasan'

urlpatterns = [
    path('show/<id_tayangan>', ulasan, name='ulasan'),
    path('show/<id_tayangan>', submit_ulasan, name='submit_ulasan')
]