from django.urls import path, include
from user.views import *

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('user_info/', UserInfo.as_view()),
    path('user_account/', ChangePassword.as_view()),
    path('identity/', GetIdentity.as_view()),
    path()
]