from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task import views

router = DefaultRouter()

router.register("tasks", views.TaskModelViewSet, basename="tasks")

urlpatterns = [
    path('', include(router.urls))
]
