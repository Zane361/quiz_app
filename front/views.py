from django.shortcuts import render, redirect
from main import models
from random import shuffle


def quiz_solve(request, code):
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        if request.POST['user_name'] and request.POST.get('email') and request.POST.get('phone') != '+998':
            answer = models.Answer.objects.create(
                quiz = quiz,
                user_name = request.POST['user_name'],
                phone = request.POST.get('phone'),
                email = request.POST.get('email')
            )
            for key, value in request.POST.items():
                if key.isdigit():
                    models.AnswerDetail.objects.create(
                        answer = answer,
                        question_id = int(key),
                        user_answer_id = int(value)
                    )
            return redirect('front:quiz_detail', answer.code)
    context = {
        'quiz':quiz,
        'questions':questions,
    }
    return render(request, 'front/quiz_solve.html', context)

def quiz_detail(request, code):
    answer = models.Answer.objects.get(code=code)
    details = models.AnswerDetail.objects.filter(answer=answer)
    correct = 0
    in_correct = 0
    for detail in details:
        if detail.is_correct:
            correct += 1
        else:
            in_correct += 1
    try:
        correct_percentage = int(correct * 100 / details.count())
    except:
        correct_percentage = 0
    in_correct_percentage = 100 - correct_percentage
    context = {
        'answer':answer,
        'details':details,
        'correct':correct,
        'in_correct':in_correct,
        'total':details.count(),
        'correct_percentage':int(correct_percentage),
        'in_correct_percentage':in_correct_percentage
    }
    return render(request, 'front/quiz_detail.html', context)
