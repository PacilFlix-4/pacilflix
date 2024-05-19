from django.urls import path
from show.views import go_to_unduhan, insert_favorit, insert_unduhan, open_ulasan, show_tayangan, show_series, show_film, show_episode, search_tayangan

app_name = 'show'

urlpatterns = [
    path('', show_tayangan, name='tayangan'),
    path('search/', search_tayangan, name='search_tayangan'),
    path('series/<series_id>', show_series, name='series'),
    path('film/<film_id>', show_film, name='film'),
    path('episode/<series_id>/<episode_number>', show_episode, name='episode'),
    path('insert_unduhan/', insert_unduhan, name='insert_unduhan'),
    path('insert_favorit/', insert_favorit, name='insert_favorit'),
    path('go_to_unduhan/', go_to_unduhan, name='go_to_unduhan'),
    path('open_ulasan/', open_ulasan, name='open_ulasan'),
]
