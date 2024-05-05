from . import serializers
from main import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser


class QuizListView(generics.ListAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer


class QuizListCreateView(generics.CreateAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminUser,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionListView(generics.ListAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
