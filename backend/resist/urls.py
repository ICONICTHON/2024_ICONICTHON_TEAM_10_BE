from django.urls import path
from .views import select_classroom,select_classroom_2,start,get_unavailable_times

urlpatterns = [
    path('select_classroom/', select_classroom),
    path('get_unavailable_times', get_unavailable_times),
    path('select_classroom_2/', select_classroom_2),
    path('start/', start),
]