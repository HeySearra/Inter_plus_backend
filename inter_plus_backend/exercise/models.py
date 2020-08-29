from django.db import models


class Exercise(models.Model):
    name = models.CharField(verbose_name='练习名', max_length=128, default='未命名')
    intro = models.CharField(verbose_name='练习介绍', max_length=128, default='')
    level = models.IntegerField(verbose_name='难度', default=0)    # 简单1，中等2，困难3，若不分，为0
    create_time = models.TimeField(verbose_name='创建时间', auto_now_add=True)
    class_id = models.IntegerField(default=0)   # 该课程的哪个课时，等于0为课前测试
    next_video_id = models.IntegerField(verbose_name='下个视频的id', default=0, blank=True)   # 即下一个课时的开始的视频

    course = models.ForeignKey('course.Course', related_name='related_exercise', verbose_name='所属课程', on_delete=models.CASCADE, null=True)
    record = models.ManyToManyField('user.User', through='Record', through_fields=('exercise', 'user'))


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
    choice_num = models.IntegerField(verbose_name='选项个数', default=0)
    blank_num = models.IntegerField(verbose_name='设空个数', default=0)
    create_time = models.TimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    alter_time = models.TimeField(verbose_name='更改时间', auto_now_add=True)
    level = models.IntegerField(default=1)  # 1易，2中，3难

    tags = models.ManyToManyField(Tag)
    exercise = models.ForeignKey('exercise.Exercise', related_name='related_question', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-create_time']


class Stem(models.Model):
    types = (('0', 'img'),
             ('1', 'markdown'))
    type = models.CharField(verbose_name='题干类型', max_length=256, choices=types, default="")
    text = models.TextField(verbose_name='md代码', default='')
    img = models.CharField(verbose_name='附加图片', max_length=4096, default='')

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='stems')


class Video(models.Model):
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)    # 视频介绍
    class_id = models.IntegerField(default=0)   # 课时数
    src = models.CharField(max_length=512)  # 视频链接

    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='related_video')


class Solution(models.Model):
    img = models.CharField(verbose_name='题解图片', max_length=4096, default='')
    type = models.CharField(verbose_name='题解类型', max_length=256, default="")

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='solutions')


class Record(models.Model):
    finished = models.BooleanField(verbose_name='是否完成', default=False)
    last_score = models.FloatField(verbose_name='最近一次作答分数', max_length=64, default=0)
    highest_score = models.FloatField(verbose_name='最高分', max_length=64, default=0)

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, related_name='related_exercise', null=True)


class Choice(models.Model):
    img = models.FileField(verbose_name='附加图片', upload_to='question/choices/', null=True, default=None, blank=True)
    name = models.CharField(verbose_name='选项名', max_length=200, default='NULL')
    if_true = models.BooleanField(verbose_name='是否正确', default=False)
    selected_freq = models.IntegerField(verbose_name='被选次数', default=0)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices', null=True)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='related_choices', null=True)

    class Meta:
        ordering = ['-id']


class Blank(models.Model):
    ord = models.IntegerField(verbose_name='设空序号', default=1)
    img = models.FileField(verbose_name='附加图片', upload_to='question/blanks', null=True, default=None, blank=True)
    answer = models.CharField(verbose_name='设空答案', max_length=256)
    type = models.CharField(verbose_name='答案类型', max_length=256, default='0')   # 0是文字，1是图片
    total = models.PositiveIntegerField(verbose_name='总回答次数', default=0)
    correct_freq = models.PositiveIntegerField(verbose_name='正确回答次数', default=0)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='blanks', null=True)

    class Meta:
        ordering = ['-id']


class SubjectQuestionAnswer(models.Model):
    answer = models.CharField(verbose_name='答案描述', max_length=64, default='', blank=True)
    img = models.CharField(verbose_name='答案图片', max_length=4096, default='')
    type = models.CharField(verbose_name='答案类型', max_length=256, default='')
    total = models.PositiveIntegerField(verbose_name='总回答次数', default=0)
    average = models.FloatField(verbose_name='平均分', default=0)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='sub_answers')


class WrongQuestion(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='wrong_question_book', null=True)
    question = models.ManyToManyField('Question', related_name='wrong_question')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True)