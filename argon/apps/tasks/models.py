from django.db import models
from argon.apps.dashboard.models import Profile #para que tenga relacion con profile


# Create your models here.
class Task(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estatus = models.BooleanField(default=True)  # True = En proceso, False = Terminada
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tasks',db_column='profile_id')

    class Meta:
        db_table = 'tasks'


