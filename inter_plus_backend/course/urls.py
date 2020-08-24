from django.urls import path, include
from course.views import *

urlpatterns = [
    path('subject_list/', GetSubjectList.as_view()),
    path('list/', GetCourseList.as_view()),
    path('user_list/', GetUserCourseList.as_view()),
    path('note_list', GetCourseNoteList.as_view()),
    path('user_note_list/', GetCourseUserNoteList.as_view()),
    path('info/', CourseInfo.as_view()),
    path('join/', JoinCourse.as_view()),
    path('like/', LikeCourse.as_view()),
    path('class_info/', ClassInfo.as_view()),
]