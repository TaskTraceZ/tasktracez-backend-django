from rest_framework import viewsets

from project.models import Project
from project.serializers import ProjectSerializer


class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer
