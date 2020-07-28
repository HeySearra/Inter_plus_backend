from django.urls import path, include
from user.views import *

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),

]