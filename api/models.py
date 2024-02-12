from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'new'
        IN_PROGRESS = 'in_progress'
        COMPLETED = 'completed'

    name = models.CharField(max_length=16)
    desc = models.CharField(max_length=256, blank=True, verbose_name='Description', default='')
    status = models.CharField(max_length=11, choices=Status, default=Status.NEW)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
