from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('api/', views.api_overview, name='api_overview'),
    path('submit-message/', views.submit_message, name='submit_message'),
]

