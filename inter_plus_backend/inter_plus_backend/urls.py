from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from course.views import *
from user.views import *
from exercise.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('admin', admin.site.urls),
    path('upload/', include([
        path('pic', UploadImage.as_view()),

    ])),
    path('user/', include([
        path('register', Register.as_view()),
        path('login', Login.as_view()),
        path('user_info', UserInfo.as_view()),
        path('user_account', ChangePassword.as_view()),
        path('identity', GetIdentity.as_view()),
        path('post_teacher', ApplyForTeacher.as_view()),
    ])),
    path('exercise/', include([
        path('course_list', CourseExerciseList.as_view()),
        path('del_exercise', DelExercise.as_view()),
        path('question', include([
            path('info', GetQuestionInfo.as_view()),
            path('choices', GetChoices.as_view()),
        ]))
    ])),
    path('subject/list', GetSubjectList.as_view()),
    path('course/', include([
        path('subject_list', GetSubjectList.as_view()),
        path('list', GetCourseList.as_view()),
        path('user_list', GetUserCourseList.as_view()),
        path('note_list', GetCourseNoteList.as_view()),
        path('user_note_list', GetCourseUserNoteList.as_view()),
        path('info', CourseInfo.as_view()),
        path('join', JoinCourse.as_view()),
        path('like', LikeCourse.as_view()),
        path('class_info', ClassInfo.as_view()),
    ])),
    path('video/info', VideoInfo.as_view()),
    path('note/info', NoteInfo.as_view()),

    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
]
