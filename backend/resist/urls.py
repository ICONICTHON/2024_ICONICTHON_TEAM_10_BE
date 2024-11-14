from django.urls import path
from .views import select_classroom,select_classroom_2,start,get_latest_reservation

urlpatterns = [
    path('select_classroom/', select_classroom),
    path('select_classroom_2/', select_classroom_2),
    path('start/', start),
    path('get_latest_reservation/', get_latest_reservation)
]