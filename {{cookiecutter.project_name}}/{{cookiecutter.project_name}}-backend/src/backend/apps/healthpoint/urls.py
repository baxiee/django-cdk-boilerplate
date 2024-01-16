from django.urls import path

from apps.healthpoint.api import HealthPointApi

app_name = "healthpoint"

urlpatterns = [
    path(
        "",
        HealthPointApi.as_view(),
        name="healthpoint",
    ),
]
