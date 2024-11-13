from django.db import models

class Torre (models.Model):
    nombreTorre = models.CharField(max_length=1)
    def __str__(self):
        return self.nombreTorre

class Departamentos (models.Model):
    idDepto = models.AutoField(primary_key=True, unique=True)
    numeroDepto = models.IntegerField()
    torre = models.ForeignKey(Torre, on_delete=models.PROTECT)
    def __str__(self):
        return self.idDepto

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
    habitante = models.ForeignKey(Habitante, on_delete=models.CASCADE)
    fechaInicio = models.DateField(auto_now=True)
    fechaTermino = models.DateField(null=True)
    def __str__(self):
        return f"{str(self.depto)}  {str(self.habitante.rut)}"
    
class Deuda (models.Model):
    idDeuda = models.AutoField(primary_key=True, unique=True)
    monto = models.IntegerField()
    fechaDeuda = models.DateField()
    fechaVencimiento = models.DateField()
    def __str__(self):
        return self.idDeuda

class Boletapago (models.Model):

    ESTADOS = [
        ('P', 'Pagado'),
        ('N', 'No Pagado'),
        ('A', 'Anulado'),
        ('R', 'Rechazado'),
    ]
    idPago = models.AutoField(primary_key=True, unique=True)
    fechaPago = models.DateTimeField()
    monto = models.ForeignKey(Deuda,on_delete=models.CASCADE)
    depto = models.ForeignKey(Departamentos,on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADOS,default= 'N')
    def __str__(self):
        return self.idPago

#Desarrollo de modelos para la implementación completa a futuro
class Trabajador(models.Model):
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
        return self.idMant 







