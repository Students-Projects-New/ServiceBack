import os, traceback, typing
from enum import Enum
from django.core.exceptions import ObjectDoesNotExist
from apps.app_academic.models import ErrorLog
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, APIException, PermissionDenied, MethodNotAllowed
from rest_framework.views import exception_handler
from rest_framework.schemas import AutoSchema

TRUST = os.environ['TRUST'] == 'TRUST'

class ConstanteTypeTag(Enum):
    AREA = 1
    PROGRAMMING = 2

class Module(Enum):
    UNKNOWN = 0
    PROJECT = 1
    ENVIRONMENT_VARIABLE = 2

class TypeException(Enum):
    WARNING = 0
    ERROR = 1
    CRITICAL = 2

class CustomException(APIException):
    def __init__(self, *args: object, module = Module.UNKNOWN) -> None:
        super().__init__(*args)
        self.module = module
        self.type = TypeException.WARNING
    
    def error(self) -> 'CustomException':
        self.type = TypeException.ERROR
        return self

    def warning(self) -> 'CustomException':
        self.type = TypeException.WARNING
        return self
    
    def from_uknown(self, exception: Exception) -> 'CustomException':
        ErrorLog.objects.create(
            msg_log = str(exception),
            error_log = traceback.format_exc()
        )

        self.type = TypeException.CRITICAL
        self.module = Module.UNKNOWN
        return self
    
    def serialize(self) -> dict:
        return {
            'module': self.module.name,
            'message': str(self),
            'type': self.type.name
        }

class Schema():
    def __init__(self, path: str, fields: list) -> None:
        self.path = path
        self.fields = fields

class DefaultSchema(AutoSchema):
    schemas: typing.Dict[str, Schema] = {}

    def publish(self, schema: Schema) -> 'DefaultSchema':
        DefaultSchema.schemas[schema.path] = schema
        return self

    def get_manual_fields(self, path, method):
        extra_fields = []

        for _path, schema in DefaultSchema.schemas.items():
            if path in _path:
                extra_fields = schema.fields

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

def custom_exception_handler(exc, context):
    response = exception_handler(exc=exc, context=context)

    if isinstance(exc, ValidationError) or isinstance(exc, ObjectDoesNotExist):
        custom_exception = CustomException('Hay problemas con los datos que esta tratando de registrar.')
    elif isinstance(exc, PermissionDenied):
        custom_exception = CustomException('No estas autorizado para realizar esta solicitud.')
    elif isinstance(exc, MethodNotAllowed):
        custom_exception = CustomException('Revisa la petición que estas realizando, {0}.'.format(response.status_text))
    elif isinstance(exc, CustomException):
        custom_exception = exc
    else:
        custom_exception = CustomException('Ha ocurrido algo malo! Por favor reintente la operación.')
        custom_exception.from_uknown(exc)

    return Response(custom_exception.error().serialize(), status=400)