from django.db import models




class User(models.Model):
    genders = (
        ('0', '未知'),
        ('1', '男'),
        ('2', '女'),
    )
    identities = (
        ('user', '普通用户'),
        ('vip', '会员'),
        ('admin', '管理员'),
    )
    name = models.CharField(max_length=128, verbose_name='姓名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(max_length=254, unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=8, verbose_name='性别', default='0', choices=genders)
    create_time = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建时间')
    profile = models.FileField(max_length=512, blank=True, upload_to='profile', verbose_name="头像")
    auth = models.CharField(max_length=128, verbose_name='身份', choices=identities, default='student')  # student, teacher, admin
    major = models.CharField(max_length=128, default='')
    school = models.CharField(max_length=128, default='')
    grade = models.IntegerField(default=0)
