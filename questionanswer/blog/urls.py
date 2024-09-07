from django.urls import path
from django.urls import path
from .views import (user_login, user_logout, user_register, index, quizList, quizDetail, question_detail, create_option,
                    delete_question, delete_option, export_answers_to_excel, export_answer_detail_to_excel, render_quiz_to_pdf)

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('', index, name='index'),
    path('quiz-list/', quizList, name='quizList'),
    path('quiz-detail/<int:id>', quizDetail, name='quizDetail'),
    path('question/<int:question_id>/', question_detail, name='question_detail'),
    path('option/create/<int:question_id>/', create_option, name='create_option'),
    path('question/delete/<int:question_id>/', delete_question, name='delete_question'),
    path('option/delete/<int:option_id>/', delete_option, name='delete_option'),
    path('quiz/<int:quiz_id>/export_answers/', export_answers_to_excel, name='export_answers_to_excel'),
    path('answer/<int:answer_id>/export_detail/', export_answer_detail_to_excel, name='export_answer_detail_to_excel'),
    path('quiz/<int:quiz_id>/render_to_pdf/', render_quiz_to_pdf, name='render_quiz_to_pdf'),
]

