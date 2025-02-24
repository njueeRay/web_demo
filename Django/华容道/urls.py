from django.urls import path
from funny_game.views import solve_puzzle

urlpatterns = [
    path('', solve_puzzle, name='solve_puzzle'),
    # ...existing code...
]
