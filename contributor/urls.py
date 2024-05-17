from django.urls import path
from contributor.views import show_contributors

app_name = 'contributor'

urlpatterns = [
path('', show_contributors, name='show_contributors'),
]