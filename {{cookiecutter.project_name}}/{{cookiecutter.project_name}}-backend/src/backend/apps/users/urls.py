from django.urls import path

from apps.users import api

app_name = "users"

urlpatterns = [
    path(
        "",
        api.UserListApi.as_view(),
        name="user-list",
    ),
]
