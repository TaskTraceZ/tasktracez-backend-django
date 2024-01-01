from datetime import datetime, timedelta

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from task_instance.models import TaskInstance
from task_instance.serializers import TaskInstanceSerializer


class TaskInstanceModelViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()

    serializer_class = TaskInstanceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_date",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The start date for filtering tasks (format: YYYY-MM-DD).",
            ),
            OpenApiParameter(
                name="end_date",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The end date for filtering tasks (format: YYYY-MM-DD).",
            ),
            OpenApiParameter(
                name="sort_by",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Sort the results by this field. (e.g., \"created_at\", \"task_title\")",
            ),
            OpenApiParameter(
                name="sort_order",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Sort order. Use \"asc\" for ascending order and \"desc\" for descending order. (default: \"asc\")",
            ),
        ],
        responses={200: TaskInstanceSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")

        if not start_date:
            return Response(
                {"error": "Missing required query parameter: start_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        end_date = request.query_params.get("end_date")

        if not end_date:
            return Response(
                {"error": "Missing required query parameter: end_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        queryset = self.get_queryset()

        queryset = queryset.filter(created_at__gte=start_date).filter(
            created_at__lte=end_date
        )

        sort_by = request.query_params.get("sort_by")
        sort_order = request.query_params.get("sort_order", "asc")

        if sort_order not in ["asc", "desc"]:
            return Response(
                {"error": "Invalid sort_order parameter. Use \"asc\" or \"desc\"."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if sort_by == "created_at":
            if sort_order == "asc":
                queryset = queryset.order_by("created_at")
            elif sort_order == "desc":
                queryset = queryset.order_by("-created_at")

        serializer = self.serializer_class(queryset, many=True)

        if sort_by == "task_title":
            data = serializer.data

            key_function = lambda x: x["task_title"]

            data = sorted(data, key=key_function, reverse=(sort_order == "desc"))

            return Response(data)

        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="started_at",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The time at which the task is started (format: HH:MM:SS).",
            ),
        ],
    )
    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        started_at = request.query_params.get("started_at")

        if not started_at:
            return Response(
                {"error": "Missing required query parameter: started_at"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        started_at = datetime.strptime(started_at, "%H:%M:%S").time()

        task = self.get_object()

        task.started_at = started_at

        task.in_progress = True

        task.save()

        serializer = self.serializer_class(task)

        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="stopped_at",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The time at which the task is stopped (format: HH:MM:SS).",
            ),
        ],
    )
    @action(detail=True, methods=["post"])
    def stop(self, request, pk=None):
        stopped_at = request.query_params.get("stopped_at")

        if not stopped_at:
            return Response(
                {"error": "Missing required query parameter: stopped_at"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        stopped_at = datetime.strptime(stopped_at, "%H:%M:%S").time()

        task = self.get_object()

        task.stopped_at = stopped_at

        started_at_to_seconds = (
            task.started_at.hour * 3600
            + task.started_at.minute * 60
            + task.started_at.second
        )
        stopped_at_to_seconds = (
            task.stopped_at.hour * 3600
            + task.stopped_at.minute * 60
            + task.stopped_at.second
        )

        task.duration_worked = task.duration_worked + timedelta(
            seconds=(stopped_at_to_seconds - started_at_to_seconds)
        )

        task.in_progress = False

        task.save()

        serializer = self.serializer_class(task)

        return Response(serializer.data)
