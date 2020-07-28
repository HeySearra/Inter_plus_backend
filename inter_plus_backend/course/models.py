from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=64)
    intro = models.CharField(max_length=512)


class Course(models.Model):
    name = models.CharField(max_length=128)
    intro = models.CharField(max_length=512)
    class_count = models.IntegerField(default=0)

    author = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='have_course')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='related_course')
    who_like = models.ManyToManyField('user.User', related_name='like_course')


class Note(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256, default='')
    content = models.TextField(verbose_name="全文", default='')
    class_id = models.IntegerField(default=0, verbose_name='课时')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name="修改时间", auto_now_add=True)
    recycle_time = models.DateTimeField(verbose_name="删除时间", null=True)

    author = models.ForeignKey('user.User', related_name="related_note", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='related_note', on_delete=models.CASCADE)