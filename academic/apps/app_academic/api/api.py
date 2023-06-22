from apps.app_academic.api.serializers import (
SubjectSerializer,
SubjectPeriodSerializer,
SubjectPeriodSerializerAll,
SubjectSerializer,
SubjectStudentSerializer,
SubjectStudentSerializerAll

)
from apps.app_academic.api.core import (
    CustomException, 
    DefaultSchema,
    TRUST
)
from rest_framework.permissions import IsAuthenticated, AllowAny
import datetime
from apps.app_academic.models import Subject, SubjectPeriod, SubjectStudent ,ErrorLog

from rest_framework.permissions import IsAuthenticated
import traceback
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class CustomException(Exception):
    pass

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, CustomException):
                ErrorLog.objects.create(
                    msg_log = str(e),
                    error_log = traceback.format_exc()
                )
                return Response({"error": "Ha ocurrido algo malo!"}, status=400)

            return Response({"error": str(e)})

    return inner_function


class SubjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    
    
    def get(self, request):
        subjects = Subject.objects.all()
        subjects_serializer = SubjectSerializer(subjects,many=True)
        return Response(subjects_serializer.data)

    
    def post(self, request,format=None):
        subject_serializer = SubjectSerializer(data=request.data,many=True)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return Response(subject_serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": "No se pudo crear la materia"},status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self,request,id_subject):
        subject = Subject.objects.filter(id=id_subject).first()
        subject_serializer = SubjectSerializer(subject,data=request.data)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return Response(subject_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"msg": "No se pudo actualizar la materia"},status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,id_subject):
        subject = Subject.objects.filter(id=id_subject).first()
        subject.delete()
        return Response({"msg":"eliminado"},status=status.HTTP_204_NO_CONTENT)
    
    
    def patch(self,request,id_subject):
        subject = Subject.objects.filter(id=id_subject).first()
        subject_serializer = SubjectSerializer(subject,data=request.data,partial=True)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return Response(subject_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"msg": "No se pudo actualizar la materia"},status=status.HTTP_400_BAD_REQUEST)
        
class SubjectPeriodView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )


    
    def get(self, request):
        subjects_period = SubjectPeriod.objects.all()
        
        subjects_period_serializer = SubjectPeriodSerializerAll(subjects_period,many=True)
        return Response(subjects_period_serializer.data)
    
    
    def post(self, request): 
        print(request.data)
        for data in request.data :
            data["id_subject"] =  Subject.objects.filter(code=str(data["id_subject"])).first().id
            data.update({
                    "period": "1" if datetime.datetime.now().month < 6 else "2",
                    "year":str(datetime.datetime.now().year)
                })
        
        subject_period_serializer = SubjectPeriodSerializer(data=request.data,many=True)
        if subject_period_serializer.is_valid():
            subject_period_serializer.save()
            return Response(subject_period_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subject_period_serializer.errors)

    
    def put(self, request, id_subject_period):

        subject_period = SubjectPeriod.objects.filter(id=id_subject_period).first()
        subject_period_serializer = SubjectPeriodSerializer(subject_period,data=request.data)
        if subject_period_serializer.is_valid():
            subject_period_serializer.save()
            return Response(subject_period_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"msg": "No se pudo actualizar la materia"},status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,id_subject_period):
        subject_period = SubjectPeriod.objects.filter(id=id_subject_period).first()
        subject_period.delete()
        return Response({"msg":"eliminado"},status=status.HTTP_204_NO_CONTENT)

class SubjectPeriodDetailView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    
    def get(self, request,id_teacher):
        subjects_period = SubjectPeriod.objects.filter(id_teacher=id_teacher)
        subjects_period_serializer = SubjectPeriodSerializerAll(subjects_period,many=True)
        return Response(subjects_period_serializer.data)
    
class SubjectPeriodDetailByIdView(APIView):

    
    def get(self, request,id_period):
        subjects_period = SubjectPeriod.objects.filter(id=id_period).first()
        subjects_period_serializer = SubjectPeriodSerializerAll(subjects_period)
        return Response(subjects_period_serializer.data)
    
   
class SubjectStudentView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    
    def get(self,request):
        subject_student = SubjectStudent.objects.all()
        subject_student_serializer = SubjectStudentSerializerAll(subject_student,many=True) 
        return Response(subject_student_serializer.data)
    
    
    def post(self,request):
        try :
            for code in request.data["students"] :
                my_data ={
                    "id_subject_period":request.data["id_subject_period"],
                    "id_student":code
                }
        
                subject_student_serializer = SubjectStudentSerializer(data=my_data)
                if (subject_student_serializer.is_valid()):
                    subject_student_serializer.save()
                    
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({"msg":"No se pudo asignar el estudiante a la materia"},status=status.HTTP_400_BAD_REQUEST)

        
    
    def delete(self,request,id_subject_student):
        subject_student = SubjectStudent.objects.filter(id=id_subject_student).first()
        subject_student.delete()
        return Response({"msg":"eliminado"},status=status.HTTP_204_NO_CONTENT)


class SubjectsStudentsPeriod(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    
    def get(self,request,id_subject_period):
        print(type(id_subject_period))
        subjects_period = SubjectPeriod.objects.get(id=id_subject_period)      
        subject_students = SubjectStudent.objects.filter(id_subject_period=subjects_period)
        students = list()
        for i in subject_students:
            students.append(i.id_student)
        print(students)

        return Response({"students":students})

class SubjectStudentDetailView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    
    def get(self,request,id_student):
        subject_student = SubjectStudent.objects.filter(id_student=id_student)
        subject_student_serializer = SubjectStudentSerializerAll(subject_student,many=True) 
        return Response(subject_student_serializer.data)