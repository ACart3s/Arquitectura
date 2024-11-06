from django.db import models

class departamentos (models.Model):
    idDepto = models.AutoField(primary_key=True, unique=True)
    numeroDepto = models.IntegerField()
    torre = models.CharField(max_length=1, unique=True)
    def _str_(self):
        return self.idDepto

class habitante (models.Model):
    TIPO = [
        ('A', 'Arrendatario'),
        ('P', 'Propietario'),
    ]
    rut = models.CharField(max_length=10, primary_key=True, unique=True)
    nombre = models.CharField(max_length=300)
    correo = models.EmailField(unique=True)
    telefono = models.IntegerField()
    contactoEmergencia = models.IntegerField()
    def _str_(self):
        return self.rut

class deptoHabitante (models.Model):
    idDepto = models.ForeignKey(departamentos, on_delete=models.CASCADE)
    rut = models.ForeignKey(habitante, on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    fechaTermino = models.DateField(null=True)
    def _str_(self):
        return self.habitante.nombre + self.departamentos.numeroDepto

class deuda (models.Model):
    idDeuda = models.AutoField(primary_key=True, unique=True)
    monto = models.IntegerField()
    fechaDeuda = models.DateField()
    fechaVencimiento = models.DateField()
    def _str_(self):
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
    monto = models.ForeignKey(deuda,on_delete=models.CASCADE)
    depto = models.ForeignKey(departamentos,on_delete=models.CASCADE)
    estado = models.CharField(max_length=1, choices=ESTADOS)
    def _str_(self):
        return self.idPago