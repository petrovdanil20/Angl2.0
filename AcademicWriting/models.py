from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Group(models.Model):
    # Name
    name = models.CharField(max_length=30, verbose_name='Group')
    # Members
    students = models.ManyToManyField(User, related_name='students')
    teachers = models.ManyToManyField(User, related_name='teachers')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Task(models.Model):
    # Technical information
    creation_date = models.DateTimeField(auto_now=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Teacher', blank=False, null=True)
    # Task parameters
    deadline = models.DateTimeField(verbose_name='Deadline', null=True)
    name = models.CharField(max_length=100, verbose_name='Task name', null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, verbose_name='Group', blank=False, null=True)
    # Essay parameters
    title = models.CharField(max_length=100, verbose_name='Title', null=True)
    words_number = models.PositiveSmallIntegerField(verbose_name='Words number', null=True)
    paragraph_number = models.PositiveSmallIntegerField(verbose_name='Paragraph number', null=True)

    def __str__(self):
        return f'{self.name}_{self.creation_date}'

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class Work(models.Model):
    # Technical information
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, verbose_name='Task', blank=False, null=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Student', blank=False, null=True)
    # Work text
    text = models.TextField(verbose_name='Text', blank=True, null=True)
    # Text analysis results
    words_number = models.PositiveSmallIntegerField(verbose_name='Words number', blank=True, null=True)
    paragraph_number = models.PositiveSmallIntegerField(verbose_name='Paragraph number', blank=True, null=True)
    mistakes_number = models.PositiveSmallIntegerField(verbose_name='Mistakes number', blank=True, null=True)
    mistakes = models.TextField(verbose_name='Mistakes', blank=True, null=True)
    specialwords_number = models.PositiveSmallIntegerField(verbose_name='Special words number', blank=True, null=True)
    specialwords = models.TextField(verbose_name='Special words', blank=True, null=True)
    # Teacher comments
    result = models.CharField(verbose_name='Result', max_length=30, blank=True, null=True)
    commentary = models.TextField(verbose_name='Commentary', blank=True, null=True)

    def __str__(self):
        return f'{self.task.name}_{self.student.get_full_name()}'

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'


class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Name')
    text = models.TextField(verbose_name='Text')

    def __str__(self):
        return f'{self.name}_{self.creation_date}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
