from typing import List
from db_app import postgres_automatization as db_postgres
from db_app import mariadb_automatization as db_mariadb
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.app_user.api.serializers import (
    ListUserByIdsSerializer, 
    UserCardSerializer, 
    EmailsSerializer,
    CreateSGBDUserSerializer,
    DatabaseSerializer,
    TypeDatabaseSerializer,
    CreateDatabaseSerializer
)
from apps.app_user.models import (
    User, 
    UserRol, 
    Rol, 
    Database, 
    TypeDatabase
)
from apps.app_user.api.core import TRUST, CustomException
from apps.app_user.constants import PROFESOR_ROL, POSTGRES_TYPE, MARIADB_TYPE

class ListUsersById(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        list_users = ListUserByIdsSerializer(data=request.data)
        if list_users.is_valid(raise_exception=True):
            list_info = User.objects.filter(id__in=list_users.validated_data['id_users'])
            list_serializer = UserCardSerializer(list_info, many=True)

            return Response(list_serializer.data, status=200)

class ListUsersIdsByEmails(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        serializer_emails = EmailsSerializer(data=request.data)
        if serializer_emails.is_valid(raise_exception=True):
            print(serializer_emails.validated_data['emails'])
            list_users = User.objects.filter(email__in=serializer_emails.validated_data['emails'])
            list_ids = []
            for user in list_users:
                list_ids.append(user.id)

            return Response({"students": list_ids}, status=200)

class UpdateRolDocente(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        serializer_emails = EmailsSerializer(data=request.data)
        if serializer_emails.is_valid(raise_exception=True):
            rol_profesor = Rol.objects.get(id=PROFESOR_ROL)
            list_users = User.objects.filter(email__in=serializer_emails.validated_data['emails'])
            for user in list_users:
                try:
                    user_rol = UserRol.objects.get(user_id=user.id)
                    user_rol.rol_id = rol_profesor
                    user_rol.save()
                except UserRol.DoesNotExist:
                    pass

            return Response(status=200)

class ListTypeDatabase(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request):
        list_types = TypeDatabase.objects.all()
        list_serialzer = TypeDatabaseSerializer(list_types, many=True)
        return Response(list_serialzer.data, status=200)

class CreateSGBDUser(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        user_db_serializer = CreateSGBDUserSerializer(data=request.data)
        if user_db_serializer.is_valid(raise_exception=True):
            user = User.objects.get(id=request.user.id) 
            if user.has_sgbd_user:
                raise CustomException("Ya tiene un usuario gestor de base de datos asignado")

            username = user.email.split("@")[0]
            password = user_db_serializer.validated_data["password"]

            db_postgres.create_user(username=username, password=password)
            db_mariadb.create_user(username=username, password=password)

            user.has_sgbd_user = True
            user.save()

            return Response(status=200)

class CreateDatabase(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        database_serializer = CreateDatabaseSerializer(data=request.data)
        if database_serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                user = User.objects.get(id=request.user.id)
                typedb = TypeDatabase.objects.get(id=database_serializer.validated_data["id_type"])

                username = user.email.split("@")[0]
                context = database_serializer.validated_data["context"]

                instance = Database()
                instance.context = context
                instance.id_user = user
                instance.type = typedb
                instance.save()

                if typedb.id == POSTGRES_TYPE:
                    db_postgres.create_database(username=username, context=context)
                    db_postgres.grant_privileges(username=username, context=context)
                else:
                    db_mariadb.create_database(username=username, context=context)
            return Response(ListDatabase._mapDatabases([instance])[0], status=200)

class ListDatabase(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request):
        list_dbs = Database.objects.filter(id_user=request.user.id)
        return Response(self._mapDatabases(list_dbs=list_dbs), status=200)
    
    @staticmethod
    def _mapDatabases(list_dbs: List[Database]) -> List[dict]:
        data = []
        for db in list_dbs:
            sub_data = {
                "id": db.id,
                "id_user": db.id_user.id,
                "context": db.context,
                "count": (
                    db_postgres.count_tables(context=db.context) 
                    if db.type.id == POSTGRES_TYPE else 
                    db_mariadb.count_tables(context=db.context)
                ),
                "type": {
                    "id": db.type.id,
                    "type": db.type.type
                }
            }
            data.append(sub_data)
        return data

class DeleteDatabase(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def delete(self, request: Request, pk_db: int):
        database = Database.objects.get(id=pk_db)
        if database.id_user.id != request.user.id:
            raise CustomException("Base de datos no encontrada")

        with transaction.atomic():
            if database.type.id == POSTGRES_TYPE:
                db_postgres.delete_database(context=database.context)
            else:
                db_mariadb.delete_database(context=database.context)
            database.delete()
        return Response(status=200)

class SearchDatabase(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, context: str):
        database_query = Database.objects.filter(context=context)
        data = ListDatabase._mapDatabases([database_query[0]])[0] if len(database_query) > 0 else {}
        return Response(data, status=200)