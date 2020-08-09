from django.urls import path

from . import views

urlpatterns = [
    path('dialogs/<sel>/messages/', views.MessagesList.as_view())
]
