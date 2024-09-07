from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import Quiz, Question, Option, Answer, AnswerDetail
from random import choice
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OptionForm

from django.http import HttpResponse
import pandas as pd
from .models import AnswerDetail, Quiz




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quizList.html')
    return render(request, 'blog/userlogin.html')


def user_logout(request):
    logout(request)
    return redirect('blog/userlogin.html')


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog/index.html')
    return render(request, 'blog/userlogin.html')


def index(request):
    return render(request, 'index.html')


def quizList(request):
    images = [
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyvnzCIKGuAtJqrrFRQLGOXW366Whmz7i05g&s',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRouBn-Kd5JlRZy7Typnzo5RGxtxnQTdpmlmg7hAxojGrA8FU-8vUKaNlSeZPpYb5pYcgs&usqp=CAU',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQiyMp1xxOrYwccMWxRCAQSgqTR-7jwCW3jDkFAa5aNOB5RXQxlRESQbKym2kWjElfRPSM&usqp=CAU',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8NOv2TrGMaOc3dK-kQoF5Qg4Yz9bs7hYUO6cBmt8TD9MuTq0hVEByGeKlRi5-vu7HV0s&usqp=CAU',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTa0YFHcwC6GKyuyLZtn46prXuvxYNVjqs0Q&s',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbUwNgaZqpH-4mihkCNDINe-pTcd4A9joj0Q&s'
    ]
    quizes = Quiz.objects.filter(author=request.user)
    quizes_img = []
    for quiz in quizes:
        quiz.img = choice(images)
        quizes_img.append(quiz)

    return render(request, 'quizList.html', {'quizes': quizes})

def quizDetail(request, id):
    quiz = Quiz.objects.get(id=id)
    return render(request, 'quizDetail.html', {'quiz': quiz})

def quizCreate(request):
    if request.method == 'POST':
        ...
    return render(request, 'quizCreate.html')


@login_required
def create_option(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = OptionForm()
    return render(request, 'create_option.html', {'form': form, 'question': question})


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'question_detail.html', {'question': question})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('quiz_list')
    return render(request, 'confirm_delete.html', {'question': question})


@login_required
def delete_option(request, option_id):
    option = get_object_or_404(Option, id=option_id)
    if request.method == 'POST':
        option.delete()
        return redirect('question_detail', question_id=option.question.id)
    return render(request, 'confirm_delete_option.html', {'option': option})





def export_answers_to_excel(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answers = AnswerDetail.objects.filter(answer__quiz=quiz)

    data = {
        'User': [answer.answer.author.username for answer in answers],
        'Question': [answer.question.name for answer in answers],
        'User Choice': [answer.user_choice.name for answer in answers],
        'Is Correct': [answer.is_correct for answer in answers],
    }
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=quiz_{quiz_id}_answers.xlsx'
    df.to_excel(response, index=False, engine='openpyxl')

    return response


def export_answer_detail_to_excel(request, answer_id):
    answer_details = AnswerDetail.objects.filter(answer_id=answer_id)

    data = {
        'Question': [detail.question.name for detail in answer_details],
        'User Choice': [detail.user_choice.name for detail in answer_details],
        'Is Correct': [detail.is_correct for detail in answer_details],
    }

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=answer_{answer_id}_details.xlsx'
    df.to_excel(response, index=False, engine='openpyxl')

    return response


from reportlab.pdfgen import canvas


def render_quiz_to_pdf(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    answers = AnswerDetail.objects.filter(answer__quiz=quiz)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=quiz_{quiz_id}_results.pdf'
    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Quiz: {quiz.name}')
    y = 750
    for answer in answers:
        p.drawString(100, y,
                     f'User: {answer.answer.author.username}, Question: {answer.question.name}, Choice: {answer.user_choice.name}, Is Correct: {answer.is_correct}')
        y -= 30

    p.showPage()
    p.save()

    return response
