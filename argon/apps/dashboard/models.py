from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    photo = models.ImageField(upload_to= 'photos')
    estatus = models.BooleanField(default=False)
    #user = models.ForeignKey(User, on_delete=models.CASCADE,db_column='id_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user', null=True, blank=True)

    class Meta:
        db_table='profile'


class Bitacora(models.Model):
    id = models.AutoField(primary_key=True)
    movimiento = models.CharField(max_length=50)
    fecha = models.DateTimeField(default=timezone.now)
    #user = models.ForeignKey(User, on_delete=models.CASCADE,db_column='id_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user', null=True, blank=True)
    class Meta:
        db_table='bitacora'