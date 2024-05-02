from django import forms
from . import models

class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = ['name', 'start_date', 'end_date']
