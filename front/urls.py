from . import views
from django.urls import path

app_name = 'front'

urlpatterns = [
    path('quiz-solve/<str:code>/', views.quiz_solve),
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz_detail')
]