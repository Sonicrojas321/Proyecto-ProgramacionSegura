from django.db import models

# Create your models here.

class Intentos(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    intentos = models.PositiveIntegerField()
    fecha_ultimo_intento = models.DateTimeField()


class TelegramBot(models.Model):
    telegram_chatID = models.CharField(max_length=256)
    telegram_token = models.CharField(max_length=256)

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=256)
    fecha_ultimo_OTP = models.DateTimeField()
    telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.DO_NOTHING, null=True)
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=150)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=150)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class Ejercicio(models.Model):
    nombre_ejercicio = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    valor = models.DecimalField(decimal_places=1, max_digits=1)
    entrada1 = models.CharField(max_length=100)
    entrada2 = models.CharField(max_length=100)
    entrada3 = models.CharField(max_length=100)
    salida1 = models.CharField(max_length=100)
    salida2 = models.CharField(max_length=100)
    salida3 = models.CharField(max_length=100)

class Respuesta(models.Model):
    respuesta = models.TextField(null=True)
    calificacion = models.DecimalField(decimal_places=1, max_digits=1)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.DO_NOTHING)
    alumno = models.ForeignKey(Alumno, on_delete=models.DO_NOTHING)