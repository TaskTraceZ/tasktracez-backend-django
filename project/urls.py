from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project import views

router = DefaultRouter()

router.register("projects", views.ProjectModelViewSet, basename="projects")

urlpatterns = [
    path('', include(router.urls))
]
