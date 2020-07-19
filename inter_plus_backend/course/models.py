from django.db import models


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    intro = models.CharField(max_length=512)


class Course(models.Model):
    id = models.AuthoField(primary_key=True)
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    class_count = models.IntegerField
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    who_like = models.ManyToManyField('user.User')
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.CASCADE)


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    class_id = models.IntegerField
    video_id = models.IntegerField
    src = models.CharField(max_length=512)
    course = models.ForeignKey(Course)
    questions = models.ForeignKey('exercise.Question')
