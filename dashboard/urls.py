from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-quiz/', views.quiz_create, name='quiz_create'),
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz_detail'),
    path('question-create/<str:code>/', views.question_create, name='question_create'),
    path('question-detail/<str:code>/', views.question_detail, name='question_detail'),
    path('question-delete/<str:code>/', views.question_delete, name='question_delete'),
    path('question-update/<str:code>/', views.question_update, name='question_update'),
    path('answer-list/<str:code>/', views.answer_list, name='answer_list'),
    path('answer-detail/<str:code>/', views.answer_detail, name='answer_detail'),
    path('excel-download/<str:code>/', views.excel_download, name='excel_download')
]