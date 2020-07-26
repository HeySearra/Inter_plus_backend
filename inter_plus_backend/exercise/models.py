from django.db import models


class Exercise(models.Model):
    name = models.CharField(verbose_name='练习名', max_length=128, default='未命名')
    intro = models.CharField(verbose_name='练习介绍', max_length=128, default='')
    level = models.IntegerField(verbose_name='难度', default=0)    # 简单1，中等2，困难3，若不分，为0
    create_time = models.TimeField(verbose_name='创建时间', auto_now_add=True)
    video_id = models.IntegerField(verbose_name='下个视频的id', default=0, blank=True)

    questions = models.ManyToManyField('question.Question')
    participants = models.ManyToManyField('user.User')
