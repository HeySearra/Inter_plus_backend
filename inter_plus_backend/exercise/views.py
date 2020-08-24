import simplejson
from django.db.models import QuerySet, Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from course.models import *
import json

from exercise.models import *
from user.models import *
from utils.response import JSR
import json
import os
import random
import string
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class CourseExerciseList(View):
    @JSR('exercises')
    def get(self, request):
        try:
            course = Course.objects.get(id=int(request.GET.get('course_id', 0)))
        except:
            return [],
        exercise_set = course.related_exercise.order_by('class_id', 'level')
        class_name_set = course.class_name_set.split('///&&&///')
        exercises = [{
            'exercise_id': e.id,
            'class_id': e.class_id,
            'name': class_name_set[e.class_id - 1],
            'create_time': e.create_time,
            'next_id': e.next_video_id,
            'author_id': course.author_id,
            'author_name': course.author.name,
            'questions': [{
                'question_id': q.id,
                'text': q.text,
                'question_type': q.question_type,
                'choice_length': q.choice_length,
                'blank_num': q.blank_num,
                'difficulty': q.difficulty,
            }for q in e.related_question.order_by('question_type', 'id')],
        }for e in exercise_set]

