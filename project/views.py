from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import Project
from project.permission import IsAdmin
from project.serializers import ProjectSerializer
from task.models import Task
from task.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


class ProjectModelViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=ProjectSerializer,
        responses={201: ProjectSerializer()},
    )
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="sort_by",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Sort the results by this field. (e.g., "title")',
            ),
            OpenApiParameter(
                name="sort_order",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Sort order. Use "asc" for ascending order and "desc" for descending order. (default: "asc")',
            ),
        ],
        responses={200: ProjectSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter(user=request.user)

        sort_by = request.query_params.get("sort_by")
        sort_order = request.query_params.get("sort_order", "asc")

        if sort_order not in ["asc", "desc"]:
            return Response(
                {"error": 'Invalid sort_order parameter. Use "asc" or "desc".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if sort_by == "title":
            if sort_order == "asc":
                queryset = queryset.order_by("title")
            elif sort_order == "desc":
                queryset = queryset.order_by("-title")

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        project = self.get_object()

        tasks = Task.objects.filter(project=project)

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
