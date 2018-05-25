"""Arkuma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from Tests import views


urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.check_test, name="check"),
    path('admin/', admin.site.urls),
    path('checkanswer/', views.check_answer, name="checkanswer"),
    path('login/', views.login, name="login"),
    path('test/theme', views.test, name="test"),
    path('stat/', views.stat, name="stat"),
    path('addPoint/', views.add_point, name="plus"),
    path('result/', views.result, name="result"),
    path('getRule/', views.get_rule, name='getRule'),
    path('getPoints/', views.get_points, name="getPoints"),
    path('<slug:type>/themes/', views.select_theme, name="select_theme"),
    path("learning/theme/", views.learning, name="theme"),
    path("registration/", views.registration, name="regisartion"),
    url(r'^tinymce/', include('tinymce.urls')),
    path("API/createStudent", views.api_registration, name="api_createstudent"),
    path('API/getQuestion/',views.api_get_question, name="api_getQuestion"),
    path('API/getQuestions/', views.api_get_questions, name="api_getQuestions"),
    path('API/switchQuestionState', views.api_switch_question_state, name="api_switch_question_state"),
    path('API/markQuestionAsLearned', views.api_mark_as_learned,name="api_marked_as_learned"),
    path('API/StudentAndQuestion/get',views.api_student_and_question_get, name="api_student_and_question_get")
]
