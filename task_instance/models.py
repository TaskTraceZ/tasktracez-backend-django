from django.db import models

from task.models import Task


class TaskInstance(models.Model):
    billable = models.BooleanField(default=False)
    started_at = models.TimeField()
    stopped_at = models.TimeField()
    duration_worked = models.DurationField()
    in_progress = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.task.title
