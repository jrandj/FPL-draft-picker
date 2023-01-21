from django.urls import path
from . import views

urlpatterns = [
    path('details/<league_id>', views.get_league_data),
    path('elements/<league_id>', views.get_element_status),
    path('bootstrap', views.get_boostrap),
    path('candidates/<league_id>/<team_name>', views.get_candidates),
]
