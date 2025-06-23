from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    """
    Manager para el modelo de Usuario personalizado.
    """
    def create_user(self, nombre_usuario, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es un campo obligatorio.')
        
        correo = self.normalize_email(correo)
        user = self.model(nombre_usuario=nombre_usuario, correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(nombre_usuario, correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de Usuario personalizado que reemplaza al de Django.
    """
    # No necesitamos id_usuario ni contraseña, Django los gestiona.
    nombre_usuario = models.CharField(max_length=40, unique=True)
    correo = models.EmailField(max_length=254, unique=True)
    
    # Campos requeridos por Django para el panel de admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Conexión con el manager
    objects = UsuarioManager()

    # Campo que se usará para el login
    USERNAME_FIELD = 'nombre_usuario'
    
    # Campos requeridos al crear un usuario por consola
    REQUIRED_FIELDS = ['correo']

    def __str__(self):
        return self.nombre_usuario

