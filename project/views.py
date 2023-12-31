from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import Project
from project.serializers import ProjectSerializer
from task.models import Task
from task.serializers import TaskSerializer


class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()

        tasks = Task.objects.filter(project=project)
        
        serializer = TaskSerializer(tasks, many=True)
        
        return Response(serializer.data)
