from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from project.urls import router as project_router
from task.urls import router as task_router
from task_instance.urls import router as task_instance_router


prefix = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        prefix,
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "schema/swagger-ui/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "schema/redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
                path("", include(project_router.urls)),
                path("", include(task_router.urls)),
                path("", include(task_instance_router.urls)),
                path("", include("user.urls")),
            ]
        ),
    ),
]
