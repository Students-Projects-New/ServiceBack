from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.db.models import FileField
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from apps.app_project.models import Project, File
from apps.app_project.api.utils import MIME_TYPE
from apps.app_project.api.core import (
    CustomException, 
    DefaultSchema,
    TRUST
)


class GetFileProjectView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, uuid_image: str):
        uuid_ext = uuid_image.split('.')
        uuid_file = uuid_ext[-1 if len(uuid_ext) < 2 else -2]

        file: FileField = None
        try:
            if 'images' in request.get_full_path():
                _project = Project.objects.filter(uuid_image=uuid_file).first()
                file = _project.image
            elif 'files' in request.get_full_path():
                _file = File.objects.filter(uuid=uuid_file).first()
                file = _file.file
            
            if file == None:
                raise Exception()
        except Exception as _:
            raise CustomException('No se encontro ningun archivo asociado')

        ext = file.path.split('.')[-1].lower()
        
        try:
            content_type = MIME_TYPE[ext]
        except:
            raise CustomException('Extensión de archivo no valida')

        with open(file.path, 'rb') as image_file:
            response = HttpResponse(FileWrapper(image_file), content_type=content_type)
        #response['Content-Disposition'] = 'attachment; filename="%s"' % (project.image.name + '.' + ext)
        return response
