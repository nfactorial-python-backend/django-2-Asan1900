#news/urls.py

from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

app_name = 'news'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:news_id>/add_comment/', views.add_comment, name='add_comment'),
    path('add/', views.add_news, name='add_news'),
    path('news_list/', views.news_list, name='news_list'),  
    path('accounts/sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:news_id>/', views.news_detail, name='news_detail'), 
]
