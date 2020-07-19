from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)
    question_type = models.IntegerField
    choice_length = models.IntegerField
    blank_num = models.IntegerField
    create_time = models.DateTimeField(auto_now=True)
    alter_time = models.DateTimeField(auto_now_add=True)
    difficulty = models.FloatField
    answer_record = models.ManyToManyField('user.User')


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    level = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now=True)
    next_id = models.IntegerField
    questions = models.ManyToManyField('Question')
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Stem(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.CharField(max_length=4096)
    text = models.CharField(max_length=1024)
    type = models.CharField(max_length=1)
    question = models.ForeignKey('Question')


class Solution(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.CharField(max_length=4096)
    text = models.CharField(max_length=1024)
    type = models.IntegerField()
    if_last = models.BooleanField()
    question = models.ForeignKey('Question')


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.FileField()
    name = models.CharField(max_length=200)
    if_true = models.BooleanField()
    video_id = models.IntegerField(default=0)
    question = models.ForeignKey('Question')


class Blank(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.FileField()
    answer = models.CharField(max_length=256)
    answer_type = models.CharField(max_length=16)
    total = models.PositiveIntegerField()
    correct_freq = models.PositiveIntegerField()
    question = models.ForeignKey('Question')


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    finished = models.BooleanField()
    if_correct = models.BooleanField()
    answer = models.CharField(max_length=64)
    sub_answer = models.FileField()
    sub_point = models.FloatField(default=0.0)
    question = models.ForeignKey('Question')
    user = models.ForeignKey('User.user', on_delete=models.CASCADE)
    exercise = models.ForeignKey('exercise.exercise', on_delete=models.CASCADE)


class SubjectQuestionAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)
    img = models.FileField()
    type = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    average = models.FloatField(default=0.0)
    question = models.ForeignKey('Question')




