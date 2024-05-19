from django.urls import path
from download.views import show_download, add_unduhan, delete_unduhan

app_name = 'download'

urlpatterns = [
    path('', show_download, name='show_download'),
    path('add/<uuid:id_tayangan>/<str:timestamp>/', add_unduhan, name='add_unduhan'),
    path('delete/<uuid:id_tayangan>/<str:timestamp>/', delete_unduhan, name='delete_unduhan'),
]