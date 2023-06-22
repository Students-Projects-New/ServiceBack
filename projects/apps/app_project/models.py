import os
from django.db import models
from enum import Enum

class Status(Enum):
    VIG = 'VIG'
    PRO = 'PRO'
    RUN = 'RUN'
    CAN = 'CAN'
    ERR = 'ERR'

class TypeJob(Enum):
    DEPLOY = 'DEPLOY'

class TypeLog(Enum):
    BUILD = os.environ["LOGS_BUILD"]
    CONT = os.environ["LOGS_CONTAINER"]

    @staticmethod
    def get(type_log: str) -> 'TypeLog':
        return TypeLog.BUILD if type_log == TypeLog.BUILD.name else TypeLog.CONT

# Create your models here.
class File(models.Model):
    uuid_file = models.CharField(max_length=100, editable=False)
    name = models.CharField(max_length=255, editable=False)
    file = models.FileField(upload_to='files/')
    size = models.FloatField(default=0)

class Project(models.Model):
    id_user = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    context = models.CharField(max_length=30, blank=False, null=False, unique=True)
    port_container = models.IntegerField(null=False)
    url = models.CharField(max_length=100, blank=False, null=False, unique=True)
    static_path = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    running = models.BooleanField(default=False)
    guid = models.CharField(max_length=255, blank=True, null=True)
    
    image = models.FileField(upload_to='images/', default=None, blank=True, null=True)
    uuid_image = models.CharField(max_length=100, blank=False, null=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectDeploy(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    id_user_deploy = models.IntegerField(blank=False, null=False)
    successful = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='VIG', blank=True, null=True)
    commit = models.TextField(blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectStatistics(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    cpu_perc = models.FloatField(default=0, blank=True, null=True)
    mem_perc = models.FloatField(default=0, blank=True, null=True)
    mem_usage = models.CharField(max_length=50, blank=True, null=True)
    mem_assign = models.CharField(max_length=50, blank=True, null=True)
    block_io_usage = models.CharField(max_length=50, blank=True, null=True)
    block_io_assign = models.CharField(max_length=50, blank=True, null=True)
    net_io_usage = models.CharField(max_length=50, blank=True, null=True)
    net_io_assign = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class ProjectCollaborator(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    id_collaborator = models.IntegerField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_project', 'id_collaborator'], name='unique_project_collaborator')
        ]

class ProjectRating(models.Model):
    class Rating(models.IntegerChoices):
        BAD = 1
        OK = 2
        GOOD = 3
        EXCELENT = 4
        AWESOME = 5

    id_user = models.IntegerField(blank=False, null=False)
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    rating = models.IntegerField(choices=Rating.choices, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_user', 'id_project'], name='unique_rating_project_user')
        ]

class StatusStage(models.Model):
    status = models.CharField(max_length=100, blank=False, null=False)

class Stage(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(StatusStage, on_delete=models.DO_NOTHING, default=1, blank=False, null=False)
    id_user = models.IntegerField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectStage(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    id_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=False, null=False)

class StageFile(models.Model):
    id_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=False, null=False)
    document = models.OneToOneField(File, on_delete=models.CASCADE, default=None, blank=True, null=True)
    id_user = models.IntegerField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

class ProjectSubject(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    id_subject_period = models.IntegerField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_project', 'id_subject_period'], name='unique_project_subject')
        ]

class EnvironmentVariable(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    name_var = models.CharField(max_length=20, blank=False, null=False)
    value_var = models.CharField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_project', 'name_var'], name='unique_project_env'),
        ]

class TypeTag(models.Model):
    name = models.CharField(max_length=255)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    type_tag = models.ForeignKey(TypeTag, on_delete=models.DO_NOTHING, blank=False, null=False)

class ProjectTag(models.Model):
    id_project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)
    id_tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_project', 'id_tag'], name='unique_tag_project'),
        ]

class ErrorLog(models.Model):
    msg_log = models.TextField(blank=True, null=True)
    error_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    guid = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    dinamico = models.TextField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=3, default='VIG', blank=True, null=True)
    progress = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

