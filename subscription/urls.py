from django.urls import path
from subscription.views import *

app_name = 'subscription'

urlpatterns = [
path('', show_main, name='show_main'),
path('buy/<str:package_name>/', show_buy_packages, name='show_buy_packages'),
path('pay/', insert_new_package, name='insert_new_package')
]