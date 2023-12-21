from rest_framework import viewsets

from task_instance.models import TaskInstance
from task_instance.serializers import TaskInstanceSerializer


class TaskInstanceModelViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()

    serializer_class = TaskInstanceSerializer
