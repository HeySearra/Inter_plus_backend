from django.db import models


class User(models.Model):
    genders = (
        ('0', '未知'),
        ('1', '男'),
        ('2', '女'),
    )
    identities = (
        ('1', '学生'),
        ('2', '老师'),
        ('3', '管理员'),
    )
    name = models.CharField(max_length=128, verbose_name='姓名')
    intro = models.CharField(max_length=512, verbose_name='介绍',default='')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(max_length=254, unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=8, verbose_name='性别', default='0', choices=genders)
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建时间')
    profile_photo = models.FileField(max_length=512, blank=True, upload_to='profile', verbose_name="头像")
    identity = models.CharField(max_length=128, verbose_name='身份', choices=identities, default='1')
    school = models.CharField(max_length=256, default='', verbose_name='学校')
    grade = models.IntegerField(default=0, verbose_name='年级')   # 若为教师，为学位

    major = models.CharField(max_length=128, default='', verbose_name='专业')
    graduate_school = models.CharField(max_length=128, default='', verbose_name='教师的毕业院校')
    teach_grade = models.IntegerField(default=0, verbose_name='教师的任教年级')


class Apply(models.Model):
    degree = models.IntegerField(default=0, verbose_name='学位')
    teach_grade = models.IntegerField(default=0, verbose_name='任教年级')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    idcard_img = models.FileField(max_length=512, blank=True, upload_to='idcard', verbose_name='身份证照片')
    xuexin_img = models.FileField(max_length=512, blank=True, upload_to='xuexin', verbose_name='学信网照片')
    teacher_img = models.FileField(max_length=512, blank=True, upload_to='teacher', verbose_name='教师资格证照片')
    reason = models.CharField(max_length=1024, default='', verbose_name='申请理由')