from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .api import SignInUpView, MyTokenRefreshView

urlpatterns = [
    path('sign_in_up/', SignInUpView.as_view()),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
