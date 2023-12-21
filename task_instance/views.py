from datetime import datetime, timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from task_instance.models import TaskInstance
from task_instance.serializers import TaskInstanceSerializer


class TaskInstanceModelViewSet(viewsets.ModelViewSet):
    queryset = TaskInstance.objects.all()

    serializer_class = TaskInstanceSerializer

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        started_at = request.query_params.get("started_at")

        if not started_at:
            return Response(
                {'error': 'Missing required query parameter: started_at'},
                status=status.HTTP_400_BAD_REQUEST
            )

        started_at = datetime.strptime(started_at, "%H:%M:%S").time()

        task = self.get_object()

        task.started_at = started_at

        task.in_progress = True

        task.save()

        serializer = self.serializer_class(task)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def stop(self, request, pk=None):
        stopped_at = request.query_params.get("stopped_at")

        if not stopped_at:
            return Response(
                {'error': 'Missing required query parameter: stopped_at'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stopped_at = datetime.strptime(stopped_at, "%H:%M:%S").time()

        task = self.get_object()

        task.stopped_at = stopped_at

        started_at_to_seconds = task.started_at.hour * 3600 + task.started_at.minute * 60 + task.started_at.second
        stopped_at_to_seconds = task.stopped_at.hour * 3600 + task.stopped_at.minute * 60 + task.stopped_at.second

        task.duration_worked = task.duration_worked + timedelta(seconds=(stopped_at_to_seconds - started_at_to_seconds))

        task.in_progress = False

        task.save()

        serializer = self.serializer_class(task)

        return Response(serializer.data)
