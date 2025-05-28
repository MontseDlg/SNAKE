from django.db import models
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    photo = models.ImageField(upload_to= 'photos')
    class Meta:
        db_table='profile'


class Bitacora(models.Model):
    id = models.AutoField(primary_key=True)
    movimiento = models.CharField(max_length=50)
    fecha = models.DateField(default=timezone.now)
    class Meta:
        db_table='bitacora'