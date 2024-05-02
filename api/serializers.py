from main import models
from rest_framework import serializers


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ['name', 'code']


class OptionSerailizer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = ['code', 'name']

        
class QuestionSerializer(serializers.ModelSerializer):
    all_options = OptionSerailizer(many=True)
    class Meta:
        model = models.Question
        fields = ['code', 'name', 'all_options']
        depth = 1


# class AnswerSerialzier(serializers.ModelSerializer):
#     class Meta:
#         model = models.Answer
#         fields = 
