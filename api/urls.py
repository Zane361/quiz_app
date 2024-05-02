from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('quiz-list/', views.QuizListView.as_view()),
    path('question-list/', views.QuestionListView.as_view()),
    path('quiz-create/', views.QuizListCreateView.as_view())
    # path('quiz-detail/<str:code>/', views.quiz_detail),
    # path('answer-create/<str:code>/', views.answer_create),
]