from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from main import models, forms
import xlsxwriter

def index(request):
    quizzes = models.Quiz.objects.filter(author=request.user.id)
    return render(request, 'dashboard/index.html', {'quizzes':quizzes})

def quiz_create(request):
    form = forms.QuizForm()
    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('dashboard:quiz_detail', quiz.code)
        else:
            form = forms.QuizForm()
    return render(request, 'dashboard/quiz/create.html', {'form':form})

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
    context = {'answers':answers, 'code':code}
    return render(request, 'dashboard/answer/answer_list.html', context)

def answer_detail(request, code):
    answer = models.Answer.objects.get(code=code)
    details = models.AnswerDetail.objects.filter(answer=answer)
    questions = models.Question.objects.filter(quiz=answer.quiz)
    correct = 0
    in_correct = questions.count()
    for detail in details:
        if detail.is_correct:
            correct += 1
            in_correct -= 1
    try:
        correct_percentage = int(correct * 100 / questions.count())
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

def excel_download(request, code):
    quiz = models.Quiz.objects.get(code=code)
    answers = models.Answer.objects.filter(quiz=quiz)
    questions_number = models.Question.objects.filter(quiz=quiz).count()

    workbook = xlsxwriter.Workbook('Natijalar.xlsx')
    worksheet = workbook.add_worksheet(str(quiz.name))
    worksheet.write(0, 0, 'Name')
    worksheet.write(0, 1, 'Phone')
    worksheet.write(0, 2, 'Email')
    worksheet.write(0, 3, 'Total Questions')
    worksheet.write(0, 4, 'Correct Answers')
    worksheet.write(0, 5, 'Incorrect Answers')

    result = []
    for answ in answers:
        answer_detail = models.AnswerDetail.objects.filter(answer=answ)
        in_correct = questions_number
        for ans in answer_detail:
            if ans.is_correct:
                in_correct -= 1
        correct = questions_number - in_correct
        result.append([answ.user_name, answ.phone, answ.email, questions_number, correct, in_correct])

    sorted_result = sorted(result, key=lambda x: x[4], reverse=True)

    for i, answer in enumerate(sorted_result):
        worksheet.write(i+1, 0, answer[0])
        worksheet.write(i+1, 1, answer[1])
        worksheet.write(i+1, 2, answer[2])
        worksheet.write(i+1, 3, answer[3])
        worksheet.write(i+1, 4, answer[4])
        worksheet.write(i+1, 5, answer[5])

    workbook.close()

    with open('Natijalar.xlsx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Natijalar.xlsx'
        return response


