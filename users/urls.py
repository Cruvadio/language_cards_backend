from django.urls import path
from .views import authenticate_user, CreateUserAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('update/', UserRetrieveUpdateAPIView.as_view()),
    path('obtain_token/', authenticate_user)
]