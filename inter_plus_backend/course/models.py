from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=64)
    intro = models.CharField(max_length=512, default='')

    class Meta:
        ordering = ['-name']


class JoinCourseMembership(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey('user.User', on_delete=models.CASCADE)

    join_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间', blank=True, null=True)
    level = models.IntegerField(default=0)  # 0不分或用户还没有做test，1简单，2中等


class Course(models.Model):
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    level = models.IntegerField(default=0)  # 是否区分用户难度，是为1，否为0
    class_count = models.IntegerField(default=0)    # 课时数
    class_name_set = models.TextField(default='')   # 课时名 用///&&&///连接
    video_id_set = models.CharField(max_length=512, default='', verbose_name='课时起始id')  # 用&&连接
    note_id_set = models.CharField(max_length=512, default='', verbose_name='官方笔记列表')   # 用&&连接，若当前课时没有笔记，也建一个空白的
    exercise_level_set = models.CharField(max_length=512, default='', verbose_name='练习难度列表')    # 用&&连接，正数为分难度（有几个分几级，为2或3），0为不分难度
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True)
    class_img = models.ImageField(upload_to='class_img/', null=True, verbose_name='课程封面')

    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='have_course', null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='related_course', null=True)
    who_like = models.ManyToManyField('user.User', related_name='like_course')
    join = models.ManyToManyField('user.User', through=JoinCourseMembership, through_fields=('course', 'student'))


class Note(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256, default='')
    content = models.TextField(verbose_name="全文", default='')
    class_id = models.IntegerField(default=0, verbose_name='课时')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name="修改时间", auto_now_add=True)
    recycle_time = models.DateTimeField(verbose_name="删除时间", null=True)

    author = models.ForeignKey('user.User', related_name="related_note", on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, related_name='related_note', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['class_id']