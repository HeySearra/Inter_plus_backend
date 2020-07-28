from django.db import models


class Tag(models.Model):
    name = models.CharField(verbose_name='知识点名称', max_length=64, unique=True)

    class Meta:
        ordering = ['name']


class Question(models.Model):
    types = (
        (1, '选择题'),
        (2, '填空题'),
        (3, '多选题'),
        (4, '不定项选择题'),
        (5, '主观题'),
    )
    text = models.CharField(verbose_name='题目描述', max_length=100, default='NULL')
    question_type = models.IntegerField(verbose_name='题目类型', choices=types, default=1)
    choice_length = models.IntegerField(verbose_name='选项个数', default=0)
    blank_num = models.IntegerField(verbose_name='设空个数', default=0)
    create_time = models.TimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    alter_time = models.TimeField(verbose_name='更改时间', auto_now_add=True)
    difficulty = models.IntegerField(default=1) # 1易，2中，3难

    tags = models.ManyToManyField(Tag)

    answer_record = models.ManyToManyField('user.User', through='Record', through_fields=('question', 'user'))

    class Meta:
        ordering = ['-create_time']


class Stem(models.Model):
    types = (('0', 'img'),
             ('1', 'markdown'))
    img = models.CharField(verbose_name='附加图片', max_length=4096, default='')     # 支持多提干
    type = models.CharField(verbose_name='题干类型', max_length=256, choices=types, default="")     # list用&&拼接

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='stems')


class Solution(models.Model):
    img = models.CharField(verbose_name='题解图片', max_length=4096, default='')
    type = models.CharField(verbose_name='题解类型', max_length=256, default="")

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='solutions')


class Choice(models.Model):
    img = models.FileField(verbose_name='附加图片', upload_to='question/choices/', null=True, default=None, blank=True)
    name = models.CharField(verbose_name='选项名', max_length=200, default='NULL')
    if_true = models.BooleanField(verbose_name='是否正确', default=False)
    selected_freq = models.IntegerField(verbose_name='被选次数', default=0)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices')


class Record(models.Model):
    finished = models.BooleanField(verbose_name='是否完成', default=False)
    time_used = models.IntegerField(verbose_name='用时(s)', default=0)
    if_correct = models.BooleanField(verbose_name='是否正确', default=False)
    answer = models.CharField(verbose_name='最近一次作答答案', max_length=64, default='')
    sub_answer = models.CharField(verbose_name='回答图片', max_length=4096, default='')
    sub_point = models.FloatField(verbose_name='得分', default=-1, blank=True)
    sub_check_img = models.FileField(verbose_name='批改结果', upload_to='question/Subjective/check', default=None, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name='题目开始时间', auto_now_add=True)     # 用于记录题目开始进行时间
    finish_time = models.DateTimeField(verbose_name='题目完成时间', auto_now_add=True)    # 用于记录题目完成时间

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    self_test = models.ForeignKey('exercise.Exercise', on_delete=models.CASCADE, related_name='question_record')


class Blank(models.Model):
    answer_types = (
        ('only', '单一答案'),
        ('range', '范围答案'),
    )
    ord = models.IntegerField(verbose_name='设空序号', default=1)
    img = models.FileField(verbose_name='附加图片', upload_to='question/blanks', null=True, default=None, blank=True)
    answer = models.CharField(verbose_name='设空答案', max_length=256)                          # 一空多答案时用&&分隔
    answer_type = models.CharField(verbose_name='答案类型', max_length=16, choices=answer_types)
    total = models.PositiveIntegerField(verbose_name='总回答次数', default=0)
    correct_freq = models.PositiveIntegerField(verbose_name='正确回答次数', default=0)

    related_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='blanks')


class SubjectQuestionAnswer(models.Model):
    # text = models.CharField(verbose_name='答案描述', max_length=64, default='', blank=True)
    img = models.CharField(verbose_name='答案图片', max_length=4096, default='')
    type = models.CharField(verbose_name='答案类型', max_length=256, default='')
    total = models.PositiveIntegerField(verbose_name='总回答次数', default=0)
    average = models.FloatField(verbose_name='平均分', default=0)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='sub_answers')