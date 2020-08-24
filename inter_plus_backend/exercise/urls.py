from django.urls import path, include
from exercise.views import *

urlpatterns = [
    path('course_list/', CourseExerciseList.as_view()),
]