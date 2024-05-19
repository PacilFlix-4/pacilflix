from django.urls import path
from favorite.views import get_daftar_favorit, get_tayangan_favorit
from favorite.views import show_favorite, show_tayangan_favorit, add_tayangan_favorit, delete_daftar_favorit, delete_tayangan_favorit

app_name = 'favorite'

urlpatterns = [
    path('get-daftar-favorit/<str:username>/', get_daftar_favorit, name='get_daftar_favorit'),
    path('get-tayangan-favorit/str:username/<str:timestamp>/', get_tayangan_favorit, name='get_tayangan_favorit'),
    path('', show_favorite, name='show_favorite'),
    path('add/<str:timestamp>/<uuid:id_tayangan>/', add_tayangan_favorit, name='add_tayangan_favorit'),
    path('delete-daftar/<str:timestamp>/', delete_daftar_favorit, name='delete_daftar_favorit'),
    path('favorit/<str:timestamp>/', show_tayangan_favorit, name='show_tayangan_favorit'),
    path('favorit/<str:timestamp>/delete-tayangan/<uuid:id_tayangan>/', delete_tayangan_favorit, name='delete_tayangan_favorit'),
]