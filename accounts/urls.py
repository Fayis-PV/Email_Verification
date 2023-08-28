from django.urls import path
from .views import *
from allauth.account.views import LogoutView,ConfirmEmailView,email_verification_sent

# app_name = 'account'
urlpatterns = [
    path('signup/',CustomSignUpView.as_view(),name='account_signup'),
    path('login/', CustomAllAuthLoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('verify-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path("confirm-email/",email_verification_sent,name="account_email_verification_sent"),
]
