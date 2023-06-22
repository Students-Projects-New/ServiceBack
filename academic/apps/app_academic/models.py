from django.db import models
from django.db.models import  UniqueConstraint

# Create your models here.

class Subject(models.Model):
    code= models.CharField(max_length=10)
    name = models.CharField(max_length=120)


class SubjectPeriod(models.Model):
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    period = models.CharField(max_length=2)
    id_teacher = models.IntegerField()
    group = models.CharField(max_length=3)
    class Meta:
        constraints = [
           UniqueConstraint(fields=['year', 'period','group','id_subject'], name='unique_class'),
        ]

class SubjectStudent(models.Model):
    id_subject_period = models.ForeignKey(SubjectPeriod,on_delete=models.CASCADE)
    id_student = models.IntegerField()

class ErrorLog(models.Model):
    msg_log = models.TextField(blank=True, null=True)
    error_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
