from django.shortcuts import render
from utils.response import JSR
import json
import os
import random
import string
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from user.hypers import *
from easydict import EasyDict
from django.views import View
from django.db.utils import IntegrityError, DataError
from user.models import User


class Register(View):
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.acc, E.pwd, E.name, E.uni = 1, 2, 3, 4

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