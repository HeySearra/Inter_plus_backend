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
            form = simplejson.loads(request.body)
            key_words = form['key_words']
            author_id = int(form['author_id'])
            subject_id = int(form['subject_id'])
            like = int(form['like'])
            join = int(form['join'])
            new = int(form['new'])
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
                       'subject_name': c.subject_name,
                       'like_count': c.who_like.count(),
                       'join_count': JoinCourseMembership.objects.filter(course=c).count(),
                       'is_join': -1 if not request.session.get('uid',
                                                                None) else 1 if JoinCourseMembership.objects.filter(
                           course=c, student_id=request.session['uid']).exists() else 0
                   } for c in cs]
               ),


class GetUserCourseList(View):
    @JSR('courses')
    def post(self, request):
        try:
            form = simplejson.loads(request.body)
            id = int(form['id'])
        except:
            return [], [],
        if id == 0:
            try:
                id = request.session['uid']
            except:
                return [], []
        cset = [a.course for a in JoinCourseMembership.objects.filter(student_id=id)]
        courses = [{
            'id': c.id,
            'name': c.name,
            'intro': c.intro,
            'class_count': c.class_count,
            'class_img': c.class_img,
            'author_id': c.author_id,
            'author_name': c.author.name,
            'subject_id': c.subject_id,
            'subject_name': c.subject_name,
            'like_count': c.who_like.count(),
            'join_count': JoinCourseMembership.objects.filter(course=c).count(),
            'is_like': 1 if id in [a.id for a in c.who_like.all()] else 0,
        } for c in cset]
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
        } for a in c.note_id_set.split('&&')]
        courses = [{
            'class_id': i + 1,
            'class_name': class_name[i],
            'note_id': note[i]['id'],
            'title': note[i]['title'],
            'create_time': note[i]['create_time'],
            'content': note[i]['content'],
        } for i in range(c.class_count)]
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
                    'create_time': Note.objects.get(id=sys_note_id[i]).create_time.strftime("%Y-%m-%d H:M:S") if
                    sys_note_id[i] != 0 else '',
                    'content': Note.objects.get(id=sys_note_id[i]).content[0:200] if sys_note_id[i] != 0 else '',
                })
        return courses


class CourseInfo(View):
    @JSR('test_id', 'name', 'intro', 'class_count', 'class_img', 'author_id', 'author_name', 'subject_id',
         'subject_name',
         'who_likes', 'who_joins', 'is_like', 'is_join', 'classes')
    def get(self, request):
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
            c = Course.objects.get(id=int(request.GET.get('id')))
        except:
            return 0, '', '', 0, '', 0, '', 0, '', 0, 0, -1, -1, 0, [],
        # exercise_ids =
        test = Exercise.objects.filter(course=c, class_id=0)
        if test.exists():
            test_id = Exercise.objects.get(course=c, class_id=0).id
        else:
            test_id = 0
        classes = []
        class_name = c.class_name_set.split('///&&&///')
        video_id = c.video_id_set.split('&&')
        note_id = c.note_id_set.split('&&')
        exercise_level = c.exercise_level_set.split('&&')
        is_join = -1 if not request.session.get('uid', None) else 1 if JoinCourseMembership.objects.filter(
            course=c, student_id=request.session['uid']).exists() else 0
        is_like = -1 if not request.session.get('uid', None) else 1 if int(request.session['uid']) in [a.id for a in
                                                                                                       c.who_like.all()] else 0
        if is_join == 1 and c.level == 1:  # 用户加入了课程且区分用户难度
            join = JoinCourseMembership.objects.get(course=c, student_id=request.session['uid'])
            user_level = join.level
        elif c.level == 0:
            user_level = 0
        else:
            user_level = -1

        for i in range(1, c.class_count + 1):
            try:
                dic = {
                    'class_index': i,
                    'class_name': class_name[i - 1],
                    'exercise_level': int(exercise_level[i - 1]),
                    'video_id': int(video_id[i - 1]),
                }
            except:
                return 0, '', '', 0, '', 0, '', 0, '', 0, 0, -1, -1, 0, [],
            if dic['exercise_level'] == 0:
                dic['exercise_id'] = Exercise.objects.get(course=c, level=0).id if Exercise.objects.filter(course=c,
                                                                                                           level=0).exists() else 0
                dic['exercise_easy_id'] = 0
                dic['exercise_middle_id'] = 0
                dic['exercise_hard_id'] = 0
            else:
                dic['exercise_id'] = 0
                dic['exercise_easy_id'] = Exercise.objects.get(course=c, level=1).id if Exercise.objects.filter(
                    course=c, level=1).exists() else 0
                dic['exercise_middle_id'] = Exercise.objects.get(course=c, level=2).id if Exercise.objects.filter(
                    course=c, level=2).exists() else 0
                dic['exercise_hard_id'] = Exercise.objects.get(course=c, level=3).id if Exercise.objects.filter(
                    course=c, level=3).exists() else 0
            if is_join == 1 and Note.objects.filter(course=c, author_id=request.session['uid'], class_id=i).exists():
                dic['note_id'] = Note.objects.get(course=c, author_id=request.session['uid'], class_id=i).id
            else:
                dic['note_id'] = note_id[i - 1]
            classes.append(dic)
        return test_id, c.name, c.intro, c.class_count, '/store/' + c.class_img.path.split('store')[1], c.author_id, \
               c.author.name, c.subject_id, c.subject.name, c.who_like.count(), JoinCourseMembership.objects.filter(
            course=c).count(), is_like, is_join, user_level, classes,


class VideoInfo(View):
    @JSR('name', 'intro', 'class_id', 'video_id', 'src', 'course_id', 'question_id')
    def get(self, request):
        try:
            video = Video.objects.get(id=int(request.GET.get('video_id')))
        except:
            return '', '', 0, 0, '', 0, 0,
        class_name = video.course.class_name_set.split('///&&&///')[video.class_id - 1]
        return class_name, video.intro, video.class_id, video.src, video.course_id, video.question_id


class LikeCourse(View):
    @JSR('status', 'new_join_num')
    def post(self, request):
        try:
            form = simplejson.loads(request.body)
            c = Course.objects.get(id=int(form['course_id']))
            op = int(form['op'])
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
            form = simplejson.loads(request.body)
            c = Course.objects.get(id=int(form['course_id']))
            op = int(form['op'])
            user = User.objects.get(id=request.session['uid'])
        except:
            return -1, 0
        join = JoinCourseMembership.objects.filter(course=c, student=user)
        if op == 1 and not join.exists():
            JoinCourseMembership.objects.create(course=c, student=user)
        elif op == 0 and join.exists():
            JoinCourseMembership.objects.get(course=c, student=user).delete()
        else:
            return -1, JoinCourseMembership.objects.filter(course=c).count()
        return 0, JoinCourseMembership.objects.filter(course=c).count()


class ClassInfo(View):
    @JSR('name', 'intro', 'class_count', 'author_id', 'author_name', 'subject_id', 'subject_name', 'like_count',
         'join_count', 'user_level', 'class_name', 'exercise_level', 'exercise_id', 'exercise_easy_id',
         'exercise_middle_id', 'exercise_hard_id', 'video_id', 'note_id')
    def get(self, request):
        try:
            c = Course.objects.get(id=int(request.GET.get('course_id')))
            class_index = int(request.GET.get('class_id'))
            user = User.objects.get(id=request.session['uid'])
        except:
            return '', '', 0, 0, '', 0, '', 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0,
        join = JoinCourseMembership.objects.filter(course=c, student=user)
        if not join.exists():
            return '', '', 0, 0, '', 0, '', 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0,
        join = join.get()
        class_name = c.class_name_set.split('///&&&///')
        video_id = c.video_id_set.split('&&')
        note_id = c.note_id_set.split('&&')
        exercise_level = c.exercise_level_set.split('&&')
        try:
            dic = {
                'class_index': class_index,
                'class_name': class_name[class_index - 1],
                'exercise_level': int(exercise_level[class_index - 1]),
                'video_id': int(video_id[class_index - 1]),
            }
        except:
            return 0, '', '', 0, '', 0, '', 0, '', 0, 0, -1, -1, 0, [],
        if dic['exercise_level'] == 0:
            dic['exercise_id'] = Exercise.objects.get(course=c, level=0).id if Exercise.objects.filter(course=c,
                                                                                                       level=0).exists() else 0
            dic['exercise_easy_id'] = 0
            dic['exercise_middle_id'] = 0
            dic['exercise_hard_id'] = 0
        else:
            dic['exercise_id'] = 0
            dic['exercise_easy_id'] = Exercise.objects.get(course=c, level=1).id if Exercise.objects.filter(
                course=c, level=1).exists() else 0
            dic['exercise_middle_id'] = Exercise.objects.get(course=c, level=2).id if Exercise.objects.filter(
                course=c, level=2).exists() else 0
            dic['exercise_hard_id'] = Exercise.objects.get(course=c, level=3).id if Exercise.objects.filter(
                course=c, level=3).exists() else 0
        if Note.objects.filter(course=c, author_id=request.session['uid'], class_id=class_index).exists():
            dic['note_id'] = Note.objects.get(course=c, author_id=request.session['uid'], class_id=class_index).id
        else:
            dic['note_id'] = note_id[class_index - 1]
        return c.name, c.intro, c.class_count, c.author_id, c.author.name, c.subject_id, c.subject.name, \
               c.who_like.count(), JoinCourseMembership.objects.filter(course=c).count(), join.level, dic['class_name'], dic[
                   'exercise_level'], dic['exercise_id'], dic['exercise_easy_id'], dic['exercise_middle_id'], dic[
                   'exercise_hard_id'], dic['video_id'], dic['note_id'],


class NoteInfo(View):
    @JSR('note')
    def get(self, request):
        try:
            uid = request.GET.get('user_id', 0)
            if uid == 0:
                uid = request.session['uid']
            note = Note.objects.filter(author_id=uid, course_id=request.GET.get('course_id'))
        except:
            return []
        res = []
        for i in note:
            res.append({'id': i.id,
                        'title': i.title,
                        'text': i.content,
                        'class_id': i.class_id})
        return res

    # def post(self, request):