from django.urls import path
from . import views

urlpatterns = [
    path('details/<league_id>', views.get_league_data),
    path('elements/<league_id>', views.get_element_status),
    path('boostrap', views.get_boostrap),
]
