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
    telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.DO_NOTHING, null=True)

class UserOTP(models.Model):
    ultimo_OTP = models.CharField(max_length=12)
    fecha_ultimo_OTP = models.DateTimeField(null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

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
    valor = models.IntegerField()
    fecha_inicio = models.DateTimeField(null=True)
    fecha_cierre = models.DateTimeField(null=True)
    entrada1 = models.CharField(max_length=100)
    entrada2 = models.CharField(max_length=100)
    entrada3 = models.CharField(max_length=100)
    salida1 = models.CharField(max_length=100)
    salida2 = models.CharField(max_length=100)
    salida3 = models.CharField(max_length=100)


class Respuesta(models.Model):
    respuesta = models.TextField(blank=True)
    calificacion = models.IntegerField(default=0)
    hora_entrega = models.DateTimeField(null=True)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.DO_NOTHING)