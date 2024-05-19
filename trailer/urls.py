from django.urls import path
from trailer.views import search_tayangan, show_episode, show_film, show_series, show_trailer 

app_name = 'trailer'

urlpatterns = [
    path('', show_trailer, name='trailer'),
    path('search/', search_tayangan, name='search_tayangan'),
    path('series/<series_id>', show_series, name='series'),
    path('film/<film_id>', show_film, name='film'),
    path('episode/<series_id>/<episode_number>', show_episode, name='episode'),
]