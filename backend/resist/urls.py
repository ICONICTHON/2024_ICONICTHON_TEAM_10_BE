from django.urls import path
from .views import select_classroom,select_classroom_1,select_classroom_2,search,start

urlpatterns = [
    path('select_classroom/', select_classroom),
    path('select_classroom_1/', select_classroom_1),
    path('select_classroom_2/', select_classroom_2),
    path('search', search),
    path('start', start),
]