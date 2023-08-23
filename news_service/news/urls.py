from django.urls import path
from django.contrib import admin
from . import views

app_name = 'news'

urlpatterns = [
    path('admin/', admin.site.urls),  # Import and include admin URLs if needed
    path('', views.news_list, name='news_list'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('add/', views.add_news, name='add_news'),
    path('news_list/', views.news_list, name='new_list'),
    path('news/', views.news_list, name='home'),
]
