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

    path('expert_support', expert_support, name= 'expert_support')





]