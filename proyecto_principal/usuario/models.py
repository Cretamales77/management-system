from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=40, unique=True)
    contraseña = models.CharField(max_length=128)
    correo = models.EmailField(max_length=254, unique=True)

    def set_password(self, raw_password):
        self.contraseña = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contraseña)

    def __str__(self):
        return self.nombre_usuario

