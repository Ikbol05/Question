from django.urls import path
from django.urls import path
from .views import (user_login, user_logout, user_register, index, quizList, quizDetail, question_detail, create_option,
                    delete_question, delete_option)

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
]