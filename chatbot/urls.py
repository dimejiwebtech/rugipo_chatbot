from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='chat_send_message'),
    path('get-history/', views.get_history, name='chat_get_history'),
]