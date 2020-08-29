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
                'choice_num': q.choice_num,
                'blank_num': q.blank_num,
                'difficulty': q.level,
            }for q in e.related_question.order_by('question_type', 'id')],
        }for e in exercise_set]


class DelExercise(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = request.GET
        if kwargs.keys() != {'exercise_id'}:
            return -1
        try:
            ex = Exercise.objects.get(id=kwargs.get('exercise_id'))
            ex.delete()
        except:
            return 1
        return 0


class GetQuestionInfo(View):
    def get(self, request):
        package = {
            "text": "GG",
            "question_type": 1,
            "choice_num": 0,
            "blank_num": 0,
            "difficulty": 0,
            "tags": [],
        }
        try:
            que = Question.objects.get(id=int(request.GET.get('id')))
        except:
            return JsonResponse(package)
        package['text'] = que.text
        package['question_type'] = que.question_type
        package['choice_num'] = que.choices.count()
        package['blanck_num'] = que.blanks.count()
        package['difficulty'] = que.level
        package['tags'] = [t.name for t in que.tags.all()]
        return JsonResponse(package)


class GetChoices(View):
    def post(self, request):
        package = {
            "choices": [],
        }
        try:
            choices = Choice.objects.get(question_id=request.GET.get('id'))
        except:
            return JsonResponse(package)
        for i in choices:
            package['choices'].append({'img': i.img, 'name': i.name, 'if_true': i.if_true,
                                       'video_id': i.video.id if i.video is not None else 0})
        return JsonResponse(package)


class GetBlanks(View):
    def post(self, request):
        package = {
            "answers": [],
        }
        try:
            que = Question.objects.get(id=int(request.POST.get('id')))
            if que.question_type == 5:
                ans = SubjectQuestionAnswer.objects.get(question=que)
            else:
                ans = Blank.objects.filter(question=que)
        except:
            return JsonResponse(package)
        for i in ans:
            package['answers'].append({'img': i.img, 'answer': i.answer, 'answer_type': i.type})
        return JsonResponse(package)


class GetWrongQuestion(View):
    def post(self, request):
        package = {
            'count': 0,
            "questions": [],
        }
        try:
            wb = WrongQuestion.objects.get(user_id=request.session['uid'], course_id=request.POST.get('course_id'))
        except:
            return JsonResponse(package)
        package['count'] = wb.question.count()
        for q in wb.question.all():
            try:
                stem = Stem.objects.get(question=q)
            except:
                return JsonResponse({'count': 0,  'questions': []})
            package['questions'].append({'question_id': q.id,
                                         'stem_type': stem.type,
                                         'stem': stem.img if stem.type == 0 else stem.text,
                                         'question_type': q.question_type,
                                         'choice_num': q.choice_num,
                                         'blank_num': q.blank_num,
                                         'difficulty': q.level})
        return JsonResponse(package)


