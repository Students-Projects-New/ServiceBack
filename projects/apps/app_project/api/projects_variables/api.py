import os
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.app_project.api.core import CustomException
from apps.app_project.models import Project, EnvironmentVariable
from apps.app_project.api.projects_variables.serializers import EnvironmentVariableSerializer
from apps.app_project.cipher import AESCipher

from apps.app_project.api.core import (
    CustomException, 
    TRUST
)

class ListEnvironmentVariableView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request, id_user, id_project):
        try:
            project = Project.objects.get(
                id_user = id_user,
                id = id_project
            )
        except Project.DoesNotExist as e:
            raise CustomException("No se encontro proyecto asociado")

        var_environments = EnvironmentVariable.objects.filter(
            id_project = project.id
        )

        vars_env_serializer = EnvironmentVariableSerializer(var_environments, many=True)
        return Response(vars_env_serializer.data)


class CreateEnvironmentVariableView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request):
        var_env_serializer = EnvironmentVariableSerializer(data=request.data)

        if var_env_serializer.is_valid():
            aes = AESCipher(os.environ["KEY_CRYPT"])

            value_crypt = aes.encrypt(var_env_serializer.validated_data["value_var"]).decode()

            var_env = var_env_serializer.save(value_var = value_crypt)
            return Response(EnvironmentVariableSerializer(var_env).data, status=200)

        return Response(var_env_serializer.errors, status=400)
    
    def delete(self, request, pk_env: int):
        try:
            var_env = EnvironmentVariable.objects.get(id=pk_env)
            var_env.delete()
            return Response(status=200)
        except EnvironmentVariable.DoesNotExist:
            raise CustomException("No hay variable de entorno asociada")