from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=64)
    intro = models.CharField(max_length=512)


class Course(models.Model):
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    class_count = models.IntegerField
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='have_course')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    who_like = models.ManyToManyField('user.User', related_name='like_course')
    exercise = models.ForeignKey('exercise.Exercise', on_delete=models.CASCADE)


class Video(models.Model):
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    class_id = models.IntegerField
    video_id = models.IntegerField
    src = models.CharField(max_length=512)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    questions = models.ForeignKey('question.Question', on_delete=models.CASCADE, related_name='question_video')
