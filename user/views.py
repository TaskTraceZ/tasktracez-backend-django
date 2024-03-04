from datetime import datetime, timedelta

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from task_instance.permission import IsMember, IsOwner
from task_instance.serializers import TaskInstanceSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdmin

from user.serializers import UserSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated, IsAdmin]
