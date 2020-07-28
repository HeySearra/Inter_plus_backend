from django.contrib import admin
from django.urls import path, include
from user.views import UploadImage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include([
        path('pic/', UploadImage.as_view()),

    ])),
    path('user/', include('user.urls')),
]
