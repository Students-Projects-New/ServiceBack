from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class TypeDatabase(models.Model):
    type = models.CharField(max_length=30, blank=True, null=True)

class Database(models.Model):
    id_user = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    context = models.CharField(max_length=30, blank=False, null=False, unique=True)
    type = models.ForeignKey(TypeDatabase, on_delete=models.DO_NOTHING, null=False)

class Rol(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, unique=True)
    picture = models.URLField(max_length=255, null=True)
    has_sgbd_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)

class UserRol(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    rol_id = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, default=1, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'rol_id'], name='unique_user_rol'),
        ]

class ErrorLog(models.Model):
    msg_log = models.TextField(blank=True, null=True)
    error_log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)