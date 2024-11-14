from django.urls import path
from .views import select_classroom,select_classroom_1,select_classroom_2,professor_classroom,search,start

urlpatterns = [
    path('select_classroom/', select_classroom.as_view()),
    path('select_classroom_1/', select_classroom_1.as_view()),
    path('select_classroom_2/', select_classroom_2.as_view()),
    path('professor_classroom', professor_classroom.as_view()),
    path('search', search.as_view()),
    path('start', start.as_view()),
]