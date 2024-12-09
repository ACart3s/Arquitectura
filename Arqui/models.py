from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    


class Torre (models.Model):
    nombreTorre = models.CharField(max_length=1)
    def __str__(self):
        return self.nombreTorre

class Departamentos (models.Model):
    numeroDepto = models.IntegerField()
    torre = models.ForeignKey(Torre, on_delete=models.PROTECT)
    def __str__(self):
        return self.torre.nombreTorre + " " + str(self.numeroDepto)

class Habitante (models.Model):
    TIPO = [
        ('A', 'Arrendatario'),
        ('P', 'Propietario'),
    ]
    rut = models.CharField(max_length=10, primary_key=True, unique=True)
    nombre = models.CharField(max_length=300)
    correo = models.EmailField(unique=True)
    telefono = models.IntegerField()
    contactoEmergencia = models.IntegerField()
    habitante_tipo = models.CharField(max_length=1, choices=TIPO, default='P')
    def __str__(self):
        return self.rut

class DeptoHabitante (models.Model):
    depto = models.ForeignKey(Departamentos, on_delete=models.PROTECT)
    habitante = models.ForeignKey(Habitante, on_delete=models.PROTECT)
    fechaInicio = models.DateTimeField()
    fechaTermino = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{str(self.depto)}  {str(self.habitante.rut)}"
    
class Deuda (models.Model):
    monto = models.BigIntegerField()
    fechaDeuda = models.DateTimeField()
    fechaVencimiento = models.DateTimeField()
    def __str__(self):
        return str(self.fechaDeuda) + " " + str(self.fechaVencimiento)

class BoletaPago (models.Model):

    ESTADOS = [
        ('P', 'Pagado'),
        ('N', 'No Pagado'),
        ('A', 'Anulado'),
        ('R', 'Rechazado'),
    ]
    fechaPago = models.DateTimeField(null=True, blank=True)
    deuda = models.ForeignKey(Deuda,on_delete=models.PROTECT)
    depto = models.ForeignKey(DeptoHabitante,on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADOS,default= 'N')
    def __str__(self):
        return self.depto.habitante.rut + " " + self.estado

#Desarrollo de modelos para la implementación completa a futuro
""" class Trabajador(models.Model):
    TIPO = [
        ('A', 'Administrador'),
        ('C', 'Conserje'),
        ('M', 'Mantenedor'),
    ]
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=300)
    run = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(unique=True)
    fechaNacimiento = models.DateField()
    fechaIngreso = models.DateField()
    trabajador_tipo = models.CharField(max_length=1, choices=TIPO, default='A')
    def __str__(self):
        return self.id
class Mantenimiento (models.Model):
    ESTADO = [
        ('P', 'Pendiente'),
        ('R', 'Realizado'),
    ]
    idMant = models.AutoField(primary_key=True, unique=True)
    fechaInicMant = models.DateTimeField()
    depto = models.ForeignKey(Departamentos,on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador,related_name='mantenimiento_trabajador',on_delete=models.CASCADE)
    descripcion = models.TextField()
    fechaTerminoMant = models.DateTimeField(null=True)
    estado_mantenimiento = models.CharField(max_length=1, choices=ESTADO, default='P')
    def __str__(self):
        return self.idMant
class HistorialMantenciones (models.Model):
    idMant = models.ForeignKey(Mantenimiento,on_delete=models.CASCADE)
    idTrabajador = models.ForeignKey(Trabajador,related_name='historial_trabajador',on_delete=models.CASCADE)
    fechaInicio = models.ForeignKey(Mantenimiento,related_name='historial_inicio', on_delete=models.CASCADE)
    fechaTermino = models.ForeignKey(Mantenimiento, related_name='historial_termino',on_delete=models.CASCADE)
    def __str__(self):
        return self.idMant  """







