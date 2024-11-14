from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_studyroom, name='search_studyroom'),
]