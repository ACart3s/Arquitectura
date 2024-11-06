from django.db import models

class Departamentos (models.Model):
    idDepto = models.AutoField(primary_key=True, unique=True)
    numeroDepto = models.IntegerField()
    torre = models.CharField(max_length=1, unique=True)
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
    depto = models.ForeignKey(Departamentos,on_delete=models.CASCADE)
    estado = models.CharField(max_length=1, choices=ESTADOS,default= 'N')
    def __str__(self):
        return self.idPago