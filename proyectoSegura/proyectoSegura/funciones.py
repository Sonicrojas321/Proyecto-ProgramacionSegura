#from django.http import HttpResponse, JsonResponse
#from django.shortcuts import render, redirect
import base64
from datetime import datetime
from datetime import timezone
import os

import requests
from db import models
from proyectoSegura import settings

def generar_salt() -> str:
    """Rutina que genera una salt aleatoria para el
    Password Hashing

    Returns:
        str: salt que se usará en el Password Hashing
    """
    p = os.urandom(6)
    salt = base64.b64encode(p).decode('utf-8')
    return salt

def obtener_ip_cliente(request) -> str:
    """Función que regresa la IP del cliente 
    de la petición dada

    Args:
        request (_type_): petición

    Returns:
        str: ip del cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def actualizar_info_cliente(cliente, intentos=1):
    fecha = datetime.now(timezone.utc)
    cliente.fecha_ultimo_intento = fecha
    cliente.intentos = intentos
    cliente.save() # update en bd

def esta_en_ventana(tiempo_ultimo_intento: datetime, ventana: int) -> bool:
    """
    Determina si una fecha dada está dento de la ventana
    de tiempo dada de acuerdo a la fecha actual

    tiempo_ultimo_intento: datetime, fecha-hora a evaluar
    ventana: int, expresada en segundos
    return: bool, True si está dentro de la ventana 
    """
    actual = datetime.now(timezone.utc)
    diferencia = (actual - tiempo_ultimo_intento).seconds
    if diferencia <= ventana:
        return True
    return False

def registrar_cliente(ip: str) -> None:
    """
    Registra la información de un cliente que
    nunca se ha visto.

    
    returns: No retorna nada, solo hará cambios en la base de datos 
    """
    fecha = datetime.now(timezone.utc)
    registro = models.Intentos(ip=ip, intentos=1,
                       fecha_ultimo_intento=fecha)
    registro.save()


def puede_loguearse(request) -> bool:
    """
    Establece si dada una petición el cliente
    tiene oportunidades para loguearse

    request: petición de Django
    return -> bool: True si tiene posibilidades
    """
    ip = obtener_ip_cliente(request)
    try:
        cliente = models.Intentos.objects.get(ip=ip)
        if not esta_en_ventana(cliente.fecha_ultimo_intento,
                           settings.LIMITE_SEGUNDOS_LOGIN):
            actualizar_info_cliente(cliente)
            return True
        # Está en la ventana y ya lo conocemos
        if cliente.intentos >= settings.LIMITE_INTENTOS_LOGIN:
            actualizar_info_cliente(cliente, cliente.intentos)
            return False
        else: # estoy en ventana y tengo intentos
            actualizar_info_cliente(cliente, cliente.intentos + 1)
            return True
        
    except: # nunca se ha visto al cliente
        registrar_cliente(ip)
        return True
    
