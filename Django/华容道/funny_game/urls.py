from django.urls import path
from . import views

urlpatterns = [
    path('solve_puzzle/', views.solve_puzzle, name='solve_puzzle'),
    # ...existing code...
]
