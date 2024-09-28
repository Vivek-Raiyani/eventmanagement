# urls.py
from django.urls import path
from .views import register_tournament, tournament_success, tournamentdetails

urlpatterns = [
    path('1/', register_tournament, name='register_tournament'),
    # Add a success view path if needed
    path('2/', tournament_success, name='tournament_success'), 
    path('3/', tournamentdetails, name='tournament'),
]
