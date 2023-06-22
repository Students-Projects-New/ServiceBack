from rest_framework import serializers
from apps.app_academic.models import Subject, SubjectPeriod, SubjectStudent 

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectPeriodSerializer(serializers.ModelSerializer):
    id_subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    

    class Meta:
        model = SubjectPeriod
        fields = ('id','year', 'period', 'id_teacher', 'group','id_subject')
        extra_kwargs = {
            "year":{'required':False},
            "period":{'required':False},
            "id_subject":{'required':False},
            }

class SubjectPeriodSerializerAll(serializers.ModelSerializer):
    id_subject = SubjectSerializer(read_only=True)

    class Meta:
        model = SubjectPeriod
        fields = ('id','year', 'period', 'id_teacher', 'group','id_subject')
    

class SubjectStudentSerializer(serializers.ModelSerializer):
    id_subject_period =  serializers.PrimaryKeyRelatedField(queryset=SubjectPeriod.objects.all())
    
    class Meta :
        model = SubjectStudent
        fields = ('id_student','id_subject_period','id')

class SubjectStudentSerializerAll(serializers.ModelSerializer):
    id_subject_period =  SubjectPeriodSerializerAll(read_only=True)
    
    class Meta :
        model = SubjectStudent
        fields = ('id','id_student','id_subject_period',)
