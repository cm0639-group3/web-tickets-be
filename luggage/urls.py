from django.urls import path
from .views import luggage_list

urlpatterns = [
    path('luggage/', luggage_list, name='luggage_list'),
]
