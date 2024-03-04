from datetime import time, timedelta
from django.db import models
from django.contrib.auth.models import User

from task.models import Task


class TaskInstance(models.Model):
    billable = models.BooleanField()
    started_at = models.TimeField(default=time(0, 0, 0))
    stopped_at = models.TimeField(default=time(0, 0, 0))
    duration_worked = models.DurationField(default=timedelta())
    in_progress = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("start_task_instance", "Can start task instance"),
            ("stop_task_instance", "Can stop task instance"),
        ]

    def __str__(self) -> str:
        return self.task.title
