from django.db import models

from task.models import Task


class TaskInstance(models.Model):
    started_at = models.DateTimeField()
    stopped_at = models.DateTimeField()
    duration_worked = models.DurationField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.task.title
