from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('details/<league_id>', cache_page(60)(views.get_league_data)),
    path('elements/<league_id>', cache_page(60)(views.get_element_status)),
    path('bootstrap', cache_page(60)(views.get_bootstrap)),
    path('candidates/<league_id>/<team_name>', cache_page(60 * 60)(views.get_candidates)),
]
