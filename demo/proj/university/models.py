from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from library.models import Library


class University(models.Model):
    name = models.CharField(max_length=50)
    libraries = models.ManyToManyField(Library, related_name='libraries')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    task_id = models.PositiveIntegerField()
    task = GenericForeignKey('content_type', 'task_id')


class Lecturer(models.Model):
    name = models.CharField(max_length=50)
    university = models.ForeignKey(University, related_name='lecturers',on_delete=models.CASCADE)

