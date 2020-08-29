from django.shortcuts import render
from utils.response import JSR
import json
import os
import random
import string
from datetime import datetime, date
from user.hypers import *
from easydict import EasyDict
from django.views import View
from django.db.utils import IntegrityError, DataError
from user.models import User, Apply


class Register(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'email', 'password', 'name'}:
            return -1,
        if '@' not in kwargs['email']:
            return -1,
        if not CHECK_PWD(kwargs['password']):
            return -1,
        if not CHECK_NAME(kwargs['name']):
            return -1,

        kwargs.update({'profile_photo': DEFAULT_PROFILE_ROOT + '\handsome.jpg'})

        try:
            u = User.objects.create(**kwargs)
        except IntegrityError:
            return -1,  # 字段unique未满足
        except DataError:
            return -1,  # 诸如某个CharField超过了max_len的错误
        except:
            return -1,
        request.session['is_login'] = True
        request.session['uid'] = u.id
        request.session.save()
        return 0,


class Login(View):
    @JSR('status')
    def post(self, request):
        if request.session.get('is_login', None):
            u = User.objects.get(request.session['uid'])
            if u.login_date != date.today():
                u.login_date = date.today()
                u.point += 5
                u.wrong_count = 0
                try:
                    u.save()
                except:
                    return -1
            return 0

        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'email', 'password'}:
            return -1

        if '@' in kwargs['email']:
            u = User.objects.filter(email=kwargs['email'])
        else:
            return -1
        if not u.exists():
            return -1
        u = u.get()

        if u.password != kwargs['password']:
            return -1

        request.session['is_login'] = True
        request.session['uid'] = u.id
        request.session['name'] = u.name
        request.session['identity'] = u.identity
        request.session.save()
        try:
            u.save()
        except:
            return -1
        return 0

    @JSR('status')
    def get(self, request):
        if request.session.get('is_login', None):
            request.session.flush()
            return 0
        else:
            return -1


class UploadImage(View):
    @JSR('url', 'status')
    def post(self, request):
        img = request.FILES.get("image", None)
        if not img:
            return '', -1

        file_name = ''.join([random.choice(string.ascii_letters + string.digits)
                             for _ in range(FNAME_DEFAULT_LEN)]) + '.' + str(img.name).split(".")[-1]
        file_path = os.path.join(DEFAULT_IMG_ROOT, file_name)
        with open(file_path, 'wb') as fp:
            [fp.write(c) for c in img.chunks()]
        return file_path, 0


class UserInfo(View):
    @JSR('status')
    def post(self, request):
        name = request.POST.get('name', '')
        intro = request.POST.get('intro', '')
        sex = request.POST.get('sex', '')
        birthday = request.POST.get('birthday', '')
        school = request.POST.get('school', '')
        major = request.POST.get('major', '')
        grade = request.POSt.get('grade', '')
        img = request.POST.get('img', '')
        graduate_school = request.POST.get('graduate_school', '')
        teach_grade = request.POST.get('teach_grade', '')
        try:
            if grade != '':
                grade = int(grade)
            if teach_grade != '':
                teach_grade = int(teach_grade)
        except:
            return -1
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return -1,
        u = u.get()

        if not 0 <= len(name) <= 64:
            return -1,
        if sex != '' and str(sex) not in GENDER_DICT.keys():
            return -1,
        if not 0 <= len(school) <= 128:
            return -1,
        if not 0 <= len(intro) <= 250:
            return -1,
        if grade != '' and not 1 <= grade <= 20:
            return -1,
        if not 0 <= len(graduate_school) <= 128:
            return -1,
        if teach_grade != '' and not 1 <= teach_grade <= 20:
            return -1,
        if name != '':
            u.name = name
        if intro != '':
            u.intro = intro
        if sex != '':
            u.sex = sex
        if birthday != '' and re.search(r'^\d{4}-\d{2}-\d{2}$', birthday):
            u.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        if school != '':
            u.school = school
        if major != '':
            u.major = major
        if grade != '':
            u.grade = grade
        if img != '':
            u.profile_photo = img
        if graduate_school != '':
            u.graduate_school = graduate_school
        if teach_grade != '':
            u.teach_grade = teach_grade

        try:
            u.save()
        except:
            return -1,
        return 0,

    @JSR('uid', 'name', 'intro', 'sex', 'birthday', 'school', 'major', 'grade', 'img', 'email', 'graduate_school',
         'teach_grade')
    def get(self, request):
        try:
            uid = request.GET['id']
            if uid == 0:
                u = User.objects.get(id=request.session['uid'])
            else:
                u = User.objects.get(id=uid)
        except:
            return 0, '', '', 0, '', '', '', 0, '', '', '', 0

        return u.id, u.name, u.intro, int(u.gender), u.birthday.strftime(
            '%Y-%m-%d'), u.school, u.major, u.grade, u.profile_photo,


class ChangePassword(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'pass_old', 'pass_new', 'email'}:
            return -1,
        try:
            u = User.objects.get(id=request.session['uid'])
        except:
            return -1,
        if u.password != kwargs['pass_old'] or u.email != kwargs['email']:
            return -1,
        else:
            u.password = kwargs['pass_new']
            try:
                u.save()
            except:
                return -1
            return 0


class GetIdentity(View):
    @JSR('identity')
    def get(self, request):
        try:
            uid = int(request.GET.get('id'))
            if uid and uid != 0:
                u = User.objects.get(id=uid)
            else:
                u = User.objects.get(id=request.session['uid'])
        except:
            return 0
        return u.identity


class ApplyForTeacher(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'degree', 'graduate_school', 'teach_grade', 'reason', 'img_per', 'img_xue', 'img_tea'}:
            return -1,
        app = Apply()
        try:
            degree = int(kwargs['degree'])
            teach_grade = int(kwargs['teach_grade'])
            u = User.objects.get(id=request.session['uid'])
        except:
            return -1
        if u.identity != '1':   # 不是学生（普通用户）
            return -1
        app.degree = degree
        u.graduate_school = kwargs['graduate_school']
        app.author = u
        app.teach_grade = teach_grade
        app.reason = kwargs['reason']
        app.idcard_img = kwargs['img_per']
        app.xuexin_img = kwargs['img_xue']
        app.teacher_img = kwargs['img_tea']
        app.save()
        u.save()
        return 0
