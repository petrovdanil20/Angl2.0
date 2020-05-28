from django.contrib import admin
from django.urls import path, re_path

from AcademicWriting import views

urlpatterns = [
    path('accounts/login', views.LoginView.as_view(), name='login_page'),
    path('tasks/accounts/login', views.LoginView.as_view(), name='login_page'),
    path('accounts/profile', views.profile, name='profile_page'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('articles/details/<int:pk>', views.ArticleDetailView.as_view(), name='article_details'),
    path('articles', views.ArticlesListView.as_view(), name='articles'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks', views.tasks, name='tasks'),
    path('tasks/task/<int:pk>/', views.task_details, name='task_details'),
    path('tasks/task/<int:pk>', views.task_details, name='task_details'),
    path('check_essay', views.checkEssay, name='check_essay'),
    re_path('', views.ArticlesListView.as_view(), name='home'),

]