from django.contrib import admin
from django.urls import path, include
from user.views import UploadImage
from course.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include([
        path('pic/', UploadImage.as_view()),

    ])),
    path('user/', include('user.urls')),
    path('exercise/', include('exercise.urls')),
    path('course/', include('course.urls')),
    path('video/info/', VideoInfo.as_view()),
]
