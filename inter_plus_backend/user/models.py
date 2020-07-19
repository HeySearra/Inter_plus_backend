from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    sex = models.IntegerField()
    create_time = models.DateTimeField(auto_now=True)
    profile = models.CharField(max_length=512)
    auth = models.IntegerField()
    major = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    grade = models.IntegerField()
    course = models.ManyToManyField('course.Course')  # ????????????????????????
    my_course = models.ManyToManyField('course.Course')
