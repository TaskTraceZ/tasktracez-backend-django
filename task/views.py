from rest_framework import viewsets

from task.models import Task
from task.serializers import TaskSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    serializer_class = TaskSerializer
