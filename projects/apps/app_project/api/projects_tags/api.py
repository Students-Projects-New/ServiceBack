import os
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from apps.app_project.api.projects_tags.serializers import (
    TagSerializer,
    ProjectTagSerializer,
)
from apps.app_project.models import (
    ProjectTag,
    TypeTag,
    Tag
)
from apps.app_project.api.core import (
    CustomException,
)

from apps.app_project.api.core import (
    CustomException, 
    ConstanteTypeTag,
    TRUST
)

class BaseListTag():
    def _list_tags(self, type_tag: TypeTag) -> TagSerializer:
        tags = Tag.objects.filter(type_tag=type_tag)
        return TagSerializer(tags, many=True)

class ListTagAreaView(APIView, BaseListTag):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    
    def get(self, request: Request):
        type_tag = TypeTag(id=ConstanteTypeTag.AREA.value)
        return Response(self._list_tags(type_tag=type_tag).data, status=200)

class ListTagProgrammingView(APIView, BaseListTag):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request):
        type_tag = TypeTag(id=ConstanteTypeTag.PROGRAMMING.value)
        return Response(self._list_tags(type_tag=type_tag).data, status=200)

class ProjectTagView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        serializer = ProjectTagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(ProjectTagSerializer(instance).data, status=200)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request: Request, pk: int):
        try:
            tag_project = ProjectTag.objects.filter(id=pk)
            tag_project.delete()
        except ProjectTag.DoesNotExist:
            raise CustomException('No se encontro tag o proyecto asociado')
        
        return Response(status=200)
