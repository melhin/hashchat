from django.urls import path
from django.views.generic import TemplateView
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('core/register/', views.RegisterView.as_view(), name='register'),
    path('core/login/', views.LoginView.as_view(), name='login'),
    path('core/logout/', views.LogoutView.as_view(), name='logout'),
]
