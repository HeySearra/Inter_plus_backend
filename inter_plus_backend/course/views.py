from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from course.models import *
import json


# Create your views here.
def get_course_info(request):
    if request.method == 'GET':
        courses = []
        query_course = Course.objects.all()
        for c in query_course:
            if c.name == request.body.name:
                courses.append(c)
    return JsonResponse({"status": 200, "courses": courses, "msg": "query courses success"})