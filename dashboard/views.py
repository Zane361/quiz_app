from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main import models

def index(request):
    quizzes = models.Quiz.objects.filter(author=request.user.id)
    return render(request, 'dashboard/index.html', {'quizzes':quizzes})

def quiz_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quiz = models.Quiz.objects.create(name=name, author=request.user)
        return redirect('dashboard:quiz_detail', quiz.code)
    return render(request, 'dashboard/quiz/create.html')

def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(quiz=quiz)
    context = {
        'quiz':quiz,
        'questions':questions
    }
    return render(request, 'dashboard/quiz/detail.html', context)

def question_create(request, code):
    quiz = models.Quiz.objects.get(code=code)
    if request.method == 'POST':
        question = models.Question.objects.create(
            name=request.POST['question'],
            quiz=quiz
            )
        models.Option.objects.create(
            name = request.POST['correct_option'],
            question = question,
            is_correct = True
        )
        for option in request.POST.getlist('options'):
            models.Option.objects.create(
            name = option,
            question = question,
            is_correct = False
            )
        return redirect('dashboard:question_detail',question.code)
    return render(request,'dashboard/question/create.html', {'quiz':quiz})

def question_detail(request, code):
    question = models.Question.objects.get(code=code)
    options = models.Option.objects.filter(question=question)
    context = {
        'question':question,
        'options':options
    }
    return render(request, 'dashboard/question/detail.html', context)

def question_delete(request, code):
    question = models.Question.objects.get(code=code)
    question.delete()
    return redirect('dashboard:quiz_detail', question.quiz.code)

def question_update(request, code):
    question = models.Question.objects.get(code=code)
    print(request.POST)
    if request.method == 'POST':
        question.name = request.POST['name']
        question.save()
        return redirect('dashboard:question_detail', question.code)

def answer_list(request, code):
    answers = models.Answer.objects.filter(quiz__code = code)
    context = {'answers':answers}
    return render(request, 'dashboard/answer/answer_list.html', context)

def answer_detail(request, code):
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
    return render(request, 'dashboard/answer/answer_detail.html', context)



"""
Quiz Create +++, List +++, Detail +++
Question Create +++, Detail ---
Option Create +++ ---
"""

