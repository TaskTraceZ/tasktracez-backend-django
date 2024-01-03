from rest_framework import viewsets

from task.models import Task
from task.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]
