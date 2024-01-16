from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/healthpoint/", include("apps.healthpoint.urls", "healthpoint")),
    path("api/users/", include("apps.users.urls", "users")),
]
