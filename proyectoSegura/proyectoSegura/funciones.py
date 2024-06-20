import base64
from datetime import datetime
from datetime import timezone
import os
import docker
import subprocess
import socket
import crypt
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
from db import models
from proyectoSegura import settings

def logueado(fun_a_decorar):
    """Manejo de sesiones, si no existe la sesión 'logueado' se regresa a '/'

    Args:
        fun_a_decorar (_type_): 
    """
    def interna(request, *args, **kwars):
        logueado = request.session.get('logueado', False)
        if not logueado:
            return redirect('/')
        return fun_a_decorar(request, *args, **kwars)
    return interna

def notoken(fun_a_decorar):
    """Manejo de sesiones, si no existe la sesión 'notoken' se regresa a '/lista', es decir que si
    ya ingresaste token, no puedes regresar a la página de generación e ingreso de Token para 2FA.

    Args:
        fun_a_decorar (_type_): 
    """
    def interna(request, *args, **kwars):
        logueado = request.session.get('notoken', False)
        if not logueado:
            return redirect('/lista/')
        return fun_a_decorar(request, *args, **kwars)
    return interna

def generar_salt() -> str:
    """Rutina que genera una salt aleatoria para el
    Password Hashing

    Returns:
        str: salt que se usará en el Password Hashing
    """
    p = os.urandom(6)
    salt = base64.b64encode(p).decode('utf-8')
    return salt

def crear_password_hasheada(password) -> str:
    """Rutina que genera el hash de la contraseña dada y regresa el hash de la misma

    Args:
        password (_type_): Contraseña a hashear

    Returns:
        str: Contraseña cifrada
    """
    configuracion = '$6$' + generar_salt()
    hasheo = crypt.crypt(password, configuracion)
    return hasheo

def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    """
    Determina si pass_a_evaluar es un password válido de acuerdo a una cadena shadow de
    entrada:

    - pass_a_evaluar: str, password de interés
    - shadow: str, cadena con el formato completo del archivo shadow, esto es:
      - $algoritmo$
      - $salt$
      - hash
     Ejemplo:
       $6$wLn3hfSJdxalxrpH$PZbtfKfDbOU07UTorvtrao4.Rvlpj1lbKFOV6wiRISPmTWptpse9SdZU/d5jd9QYSxpR41z1cqbp2x9Z.IPa3/

    
    returns: bool, True si el password es válido
    """
    _, algoritmo, salt, _ = shadow.split('$')
    configuracion = '$%s$%s$' % (algoritmo, salt)
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)
    return shadow_nuevo == shadow

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
    """Rutina que actualiza la información del cliente cuando intenta logearse

    Args:
        cliente (_type_): ---
        intentos (int, optional): Número de intentos de login. Defaults to 1.
    """
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

def validar_token(user, tokensito) -> bool:
    """Rutina que valida si el token es aceptado o no, tomado en cuenta el tiempo de vida del token
    y si el token coinciden con el que ingreso el usuario, a la vez que se elimina el token de la
    base de datos

    Args:
        user (_type_): Usuario que se está logrando
        tokensito (_type_): Token ingresado por el usuario

    Returns:
        bool: Regresa si es valido o no 
    """
    try:
        token = models.UserOTP.objects.get(usuario=user)
        print(esta_en_ventana(token.fecha_ultimo_OTP, settings.LIMITE_SEGUNDOS_TOKEN))
        if esta_en_ventana(token.fecha_ultimo_OTP, settings.LIMITE_SEGUNDOS_TOKEN) and tokensito == token.ultimo_OTP:
            token.delete()
            return True
        else:
            token.delete()
            return False
    except models.UserOTP.DoesNotExist:
        return False

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
        
    except models.Intentos.DoesNotExist: # nunca se ha visto al cliente
        registrar_cliente(ip)
        return True

def crear_archivo_entrada(ejercicio: object) -> None:
    """Rutina que crea de manera local el archivo de entrada necesario para la evaluación
    del ejercicio, tomando los datos de la base de datos.

    Args:
        ejercicio (object): Ejercicio selecionado
    """
    lista_entradas_salidas = []
    lista_entradas_salidas.append(ejercicio.entrada1)
    lista_entradas_salidas.append(ejercicio.salida1)
    lista_entradas_salidas.append(ejercicio.entrada2)
    lista_entradas_salidas.append(ejercicio.salida2)
    lista_entradas_salidas.append(ejercicio.entrada3)
    lista_entradas_salidas.append(ejercicio.salida3)

    with open("./tareas/entrada.txt", "w") as archivo_entrada:
        contador = 0
        for cadena in lista_entradas_salidas:
            archivo_entrada.write(cadena)
            if contador == 0:
                archivo_entrada.write("\n!!!!!!\n")
                contador += 1
            elif contador == 1:
                archivo_entrada.write("\n$$$$$$\n")
                contador = 0

def crear_archivo_alumno(respuesta: object) -> None:
    """Rutina que crea de manera local el archivo de respuesta del alumno (en python)

    Args:
        respuesta (object): Respuesta del alumno seleccionada
    """
    with open("./tareas/respuesta.py", "w") as archivo_python:
        archivo_python.write(respuesta.respuesta)
    

def calificar_ejercicio(respuesta: object, ejercicio: object) -> int:
    """Rutina que califica el ejercicio y regresa el valor en número de la respuesta,
    manda una señal a través de un socket UDP al contenedor dedicado para revisión de 
    código y se obtienen los logs de dicho contenedor.

    Args:
        respuesta (object): Respuesta de alumno
        ejercicio (object): Ejercicio seleccionado

    Returns:
        int: Calificación del ejercicio con la respuesta dada
    """
    crear_archivo_entrada(ejercicio)
    crear_archivo_alumno(respuesta)
    
    #Mandar señal a contenedor de tareas

    mandarSignal('tareas_segura', 34343, 'Ejecutar')
    
    cliente = docker.from_env() 
    contenedor = cliente.containers.get('proyecto-programacionsegura-tareas_segura-1')

    contenedor.wait()

    logs = contenedor.logs()
    return obtener_calificacion(logs.decode('utf-8'))

def obtener_calificacion(resultado:str) -> int:
    """Rutina encargada de obtener los logs del contenedor de revisión de tareas
    para contar cuántos casos son True y regresas en número entero la cantidad de
    True hay. 

    Args:
        resultado (str): Logs del contenedor

    Returns:
        int: Número entero con el número de True
    """
    
    resultados_logs = resultado.split("\n")

    ultimo_resultado = resultados_logs[-2] #

    resultados_limpia = ultimo_resultado[1:-1]

    resultados = resultados_limpia.split(",") #

    print(resultados)
    for i in range(len(resultados)):
        resultados[i] = resultados[i].lstrip()
    print(resultados.count('True'))

    return resultados.count('True')

def mandarSignal(hostname:str, puerto:int, signal:str):
    """Rutina de creación de socket UDP para la comunicación con otros contenedores.

    Args:
        hostname (str): Nombre de dominio
        puerto (int): Número de puerto
        signal (str): Texto, señal que se manda
    """
    #Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Dirección del destino
    direccion_destino = (hostname, puerto)

    #Enviar la señal
    mensaje = signal
    sock.sendto(mensaje.encode(), direccion_destino)

    #Cerrar el socket
    sock.close()
