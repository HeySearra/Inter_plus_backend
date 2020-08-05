from django.db.models import QuerySet, Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from course.models import *
import json

from exercise.models import Exercise
from user.models import User
from utils.response import JSR
import json
import os
import random
import string
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class GetSubjectList(View):
    @JSR('subject')
    def get(self, request):
        su = Subject.objects.all()
        a = []
        for i in su:
            a.append({'id': i.id, 'name': i.name, 'intro': i.intro})
        return a,


class GetCourseList(View):
    @JSR('course')
    def post(self, request):
        try:
            key_words = request.POST.get('key_words', [])
            author_id = request.POST.get('author_id', 0)
            subject_id = request.POST.get('subject_id', 0)
            like = request.POST.get('like', 0)
            join = request.POST.get('join', 0)
            new = request.POST.get('new', 0)
        except:
            return [],
        cset: QuerySet = Course.objects.all()[0:0]
        for k in key_words.split():
            if author_id != 0 and subject_id != 0:
                cset = cset.union(Course.objects.filter(
                    Q(author_id=author_id) & Q(subject_id=subject_id) &
                    (Q(name__icontains=k) | Q(intro__icontains=k) | Q(subject__name__icontains=k)
                     | Q(subject__intro__icontains=k))
                ))
            elif author_id != 0:
                cset = cset.union(Course.objects.filter(
                    author_id=author_id &
                    (Q(name__icontains=k) | Q(intro__icontains=k) | Q(subject__name__icontains=k)
                     | Q(subject__intro__icontains=k))
                ))
            elif subject_id != 0:
                cset = cset.union(Course.objects.filter(
                    subject_id=subject_id &
                    (Q(name__icontains=k) | Q(intro__icontains=k) | Q(subject__name__icontains=k)
                     | Q(subject__intro__icontains=k))
                ))
            else:
                cset = cset.union(Course.objects.filter(
                    Q(name__icontains=k) | Q(intro__icontains=k) | Q(subject__name__icontains=k)
                    | Q(subject__intro__icontains=k)))
        if like != 0:
            cs = sorted(
                [c for c in cset], key=lambda c: c.who_like.count()
            )
        elif join != 0:
            cs = sorted(
                [c for c in cset], key=lambda c: c.who_join.count()
            )
        elif new != 0:
            cs = sorted(
                [c for c in cset], key=lambda c: c.create_time
            )
        else:
            cs = [c for c in cset]
        return (
            [{
                'id': c.id,
                'name': c.name,
                'intro': c.intro,
                'class_count': c.class_count,
                'class_img': c.class_img,
                'author_id': c.author_id,
                'author_name': c.author.name,
                'subject_id': c.subject_id,
                'who_like_ids': [a.id for a in c.who_like.all()],
                'who_join_ids': [a.id for a in c.who_join.all()],
                'exercise_ids': [],
                'video_ids': [],
            }for c in cs]
        ),


class GetUserCourseList(View):
    @JSR('courses')
    def post(self, request):
        def get_exercise_ids(a=Course()):
            i = 1
            c = []
            for b in sorted([c for c in a.related_exercise.all()], key=lambda e: -e.class_id):
                c.append(0 if b.class_id != i else b.id)
                i = i + 1
            if len(c) != a.class_count:
                for i in range(len(c), a.class_count):
                    c.append(0)
            return c

        try:
            id = int(request.POST.get('id', 0))
        except:
            return [], [],
        if id == 0:
            try:
                id = request.session['id']
            except:
                return [], []
        cset = User.objects.get(id=id).join_course.all()
        courses = [{
            'id': a.id,
            'name': a.name,
            'intro': a.intro,
            'class_count': a.class_count,
            'class_img': '/store' + a.class_img.path.split('store')[1],
            'author_id': a.author_id,
            'subject_id': a.subject_id,
            'who_like_ids': [b.id for b in a.who_like.all()],
            'exercise_ids': get_exercise_ids(a),
            'video_ids':a.video_id_set.split('&&'),
        }for a in cset]
        return courses


class GetCourseNoteList(View):
    @JSR('courses')
    def get(self, request):
        try:
            c = Course.objects.get(id=int(request.GET.get('course_id')))
        except:
            return []
        class_name = c.class_name_set.split('///&&&///')
        note = [{
            'id': a,
            'title': Note.objects.get(id=int(a)).title if a != '0' else '暂无笔记',
            'create_time': Note.objects.get(id=int(a)).create_time.strftime("%Y-%m-%d H:M:S") if a != '0' else '',
            'content': Note.objects.get(id=int(a)).content[0:200] if a != '0' else '',
        }for a in c.note_id_set.split('&&')]
        courses = [{
            'class_id': i+1,
            'class_name': class_name[i],
            'note_id': note[i]['id'],
            'title': note[i]['title'],
            'create_time': note[i]['create_time'],
            'content': note[i]['content'],
        }for i in range(c.class_count)]
        return courses


class GetCourseUserNoteList(View):
    @JSR('courses')
    def get(self, request):
        try:
            user = User.objects.get(request.session['uid'])
            c = Course.objects.get(request.GET.get('course_id'))
        except:
            return []
        note_set = sorted([a for a in Note.objects.filter(author=user, course=c)], key=lambda e: e.class_id)
        sys_note_id = list(map(lambda e: int(e), c.note_id_set.split('&&')))
        courses = []
        index = 0
        for i in range(1, 1 + c.class_count):
            if note_set[index].class_id == i:
                courses.append({
                    'note_id': note_set[index].id,
                    'is_diy': 1,
                    'title': note_set[index].title,
                    'create_time': note_set[index].create_time.strftime("%Y-%m-%d H:M:S"),
                    'content': note_set[index].content[0:200],
                })
                index = index + 1
            else:
                courses.append({
                    'note_id': sys_note_id[i],
                    'is_diy': 0,
                    'title': Note.objects.get(id=sys_note_id[i]).title if sys_note_id[i] != 0 else '暂无笔记',
                    'create_time': Note.objects.get(id=sys_note_id[i]).create_time.strftime("%Y-%m-%d H:M:S") if sys_note_id[i] != 0 else '',
                    'content': Note.objects.get(id=sys_note_id[i]).content[0:200] if sys_note_id[i] != 0 else '',
                })
        return courses


class CourseInfo(View):
    @JSR('name', 'intro', 'class_count', 'class_img', 'author_id', 'subject_id', 'subject_name', 'who_likes', 'who_joins', 'is_like', 'is_join', 'exercise_ids', 'video_ids', 'class_names', 'note_ids')
    def get(self, request):
        try:
            c = Course.objects.get(id=int(request.GET.get('id')))
        except:
            return '', '', 0, '', 0, 0, '', 0, 0, -1, -1, [], [], [], []



class LikeCourse(View):
    @JSR('status', 'new_join_num')
    def post(self, request):
        try:
            c = Course.objects.get(id=int(request.POST.get('course_id')))
            op = int(request.POST.get('op'))
            user = User.objects.get(id=request.session['uid'])
        except:
            return -1, 0
        if op == 1 and user not in c.who_like.all():
            c.who_like.add(user)
        elif op == 0 and user in c.who_like.all():
            c.who_like.remove(user)
        else:
            return -1, c.who_like.count()
        c.save()
        return 0, c.who_like.count()


class JoinCourse(View):
    @JSR('status', 'new_like_num')
    def post(self, request):
        try:
            c = Course.objects.get(id=int(request.POST.get('course_id')))
            op = int(request.POST.get('op'))
            user = User.objects.get(id=request.session['uid'])
        except:
            return -1, 0
        if op == 1 and user not in c.join.all():
            c.join.add(user)
        elif op == 0 and user in c.join.all():
            c.join.remove(user)
        else:
            return -1, c.join.count()
        c.save()
        return 0, c.join.count()