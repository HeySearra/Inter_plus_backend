from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=64)
    intro = models.CharField(max_length=512, default='')

    class Meta:
        ordering = ['-name']


class Course(models.Model):
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    class_count = models.IntegerField(default=0)    # 课时数
    class_name_set = models.TextField(default='')   # 课时名 用///&&&///连接
    video_id_set = models.CharField(max_length=512, default='', verbose_name='课时起始id')  # 用&&连接
    note_id_set = models.CharField(max_length=512, default='', verbose_name='官方笔记列表')   # 用&&连接，若当前课时没有笔记，也建一个空白的
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True)
    class_img = models.ImageField(upload_to='class_img/', null=True, verbose_name='课程封面')

    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='have_course')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='related_course')
    who_like = models.ManyToManyField('user.User', related_name='like_course')
    who_join = models.ManyToManyField('user.User', related_name='join_course')


class Note(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256, default='')
    content = models.TextField(verbose_name="全文", default='')
    class_id = models.IntegerField(default=0, verbose_name='课时')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name="修改时间", auto_now_add=True)
    recycle_time = models.DateTimeField(verbose_name="删除时间", null=True)

    author = models.ForeignKey('user.User', related_name="related_note", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='related_note', on_delete=models.CASCADE)