from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users import models

User = get_user_model()


class UserListApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.CustomUser
            fields = ["id"]

    def get(self, request):
        users = models.CustomUser.objects.all()
        output_serializer = self.OutputSerializer(users, many=True)
        return Response(output_serializer.data)
