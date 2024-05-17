from django.urls import path
from show.views import show_tayangan, show_series, show_film, show_episode

app_name = 'show'

urlpatterns = [
    path('tayangan/', show_tayangan, name='tayangan'),
    path('series/<series_id>', show_series, name='series'),
    path('film/<film_id>', show_film, name='film'),
    path('episode/<series_id>/<episode_number>', show_episode, name='episode'),
]
