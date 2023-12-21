from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task_instance import views

router = DefaultRouter()

router.register("task_instance", views.TaskInstanceModelViewSet, basename="task_instance")

urlpatterns = [
    path('', include(router.urls))
]
