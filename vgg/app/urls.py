from django.urls import path

from .views import *



urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home_page', home_page, name='home_page'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('refresh_login', refresh_login, name='refresh_login'),
    path('change_password', change_password, name='change_password'),
    path('account_signup', account_signup, name='account_signup'),

    path('profile_page', profile_page, name='profile_page'),

    path('ask_questions', ask_questions, name='ask_questions'),
    path('all_courses', all_courses, name='all_courses'),
    path('all_tests', all_tests, name='all_tests'),
    path('all_questions', all_questions, name='all_questions'),
    path('create_course', create_course, name='create_course'),
    path('create_test', create_test, name='create_test'),
    path('single_course', single_course, name='single_course'),
    path('single_test', single_test, name='single_test'),





]