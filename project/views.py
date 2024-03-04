from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import Project, ProjectUser
from project.permission import IsAdmin
from project.serializers import ProjectSerializer
from task.models import Task
from task.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import User


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

    @action(detail=True, methods=["post"], url_path="add/(?P<user_id>[^/.]+)")
    @extend_schema(
        request=None,
        responses={200: {"message": "User added to project successfully"}},
    )
    def add_user(self, request, pk=None, user_id=None):
        project = self.get_object()

        user = User.objects.get(pk=user_id)

        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if project.user == user:
            return Response(
                {"error": "User already added to this project"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ProjectUser(project=project, user=user).save()

        return Response(
            {"message": "User added to project successfully"},
            status=status.HTTP_200_OK,
        )
