#Views.py
from datetime import datetime
from datetime import timezone
import re, requests
from django.contrib import messages
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db import models
from . import settings
from . import funciones, bot_tele
import logging

logging.basicConfig(filename='/code/proyectoSegura/app_segura2024.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


def login(request) -> HttpResponse:
    """Vista de logeo para usuarios, autentica profesores
    y alumnos en el mismo logeo

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    if request.method == 'GET':
        ip = funciones.obtener_ip_cliente(request)
        return render(request,"login.html", {'ip':ip})
    elif request.method == 'POST':
        if not funciones.puede_loguearse(request):
            error = 'Agotaste tu límite de intentos, debes esperar %s segundos' % settings.LIMITE_SEGUNDOS_LOGIN
            return render(request, 'login.html', {'errores': error})
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.Usuario.objects.get(username=username)
            if funciones.password_valido(password, user.password):
                if models.Alumno.objects.filter(usuario=user).exists():
                    user_type = 'alumno'
                elif models.Profesor.objects.filter(usuario=user).exists():
                    user_type = 'profesor'
                else:
                    error = 'Credenciales inválidas'
                    logging.error('%s falló autenticación' % funciones.obtener_ip_cliente(request))
                    return render(request, 'login.html', {'errores': error})
                #Usuario autenticado
                request.session['usuario'] = user.id
                request.session['user_type'] = user_type
                request.session["notoken"] = True
                logging.info('%s ha ingresado credenciales correctamente' % funciones.obtener_ip_cliente(request))
                return redirect('/doblefactor/')
            else:
                error = 'Credenciales inválidas'
                logging.error('%s falló autenticación' % funciones.obtener_ip_cliente(request))
                return render(request, 'login.html', {'errores': error})

        except models.Usuario.DoesNotExist:
            error = 'Credenciales inválidas'
            logging.error('%s falló autenticación' % funciones.obtener_ip_cliente(request))
            return render(request, 'login.html', {'errores': error})


def registrar_alumno(request):
    """Vista para registro de usuarios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    if request.method == 'GET':
        logging.info(funciones.obtener_ip_cliente(request) + ' ha ingresado a Registro de alumno')
        return render(request, "registro.html")
    if request.method == 'POST':
        nombre = request.POST.get('nombreAlumno')
        apellidos = request.POST.get('apellidosAlumno')
        usuario = request.POST.get('usuarioAlumno')
        contrasena = request.POST.get('contrasenaAlumno')
        confirm_contrasena = request.POST.get('contrasenaAlumno1')
        tokenusuario = request.POST.get('token_Usuario')
        botchat = request.POST.get('bot_Usuario')

        # Validación del reCAPTCHA
        
#        data = {
#            'secret': settings.RECAPTCHA_PRIVATE_KEY,
#            'response': recaptcha_response
#        }
#        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
#        result = r.json()
#
#        if not result.get('success'):
#            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
#            return render(request, 'registro.html', {'nombreAlumno': nombre, 'apellidosAlumno': apellidos, 'usuarioAlumno': usuario})

        # Validación de la contraseña
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$', contrasena):
            messages.error(request, 'La contraseña debe tener al menos 10 caracteres, incluyendo mayúsculas, minúsculas, dígitos y al menos un carácter especial.')
            return render(request, 'registro.html', request.POST)

        if contrasena != confirm_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html', request.POST)

        # Crear el usuario y el alumno
        contrasena = funciones.crear_password_hasheada(contrasena)
        nuevo_telegram_bot = models.TelegramBot(
            telegram_chatID=botchat,
            telegram_token=tokenusuario,
        )
        nuevo_usuario = models.Usuario(
            username=usuario,
            password=contrasena,
            telegram_bot=nuevo_telegram_bot
        )
        nuevo_alumno = models.Alumno(
            nombre=nombre,
            apellido=apellidos,
            usuario=nuevo_usuario
        )
        nuevo_telegram_bot.save()
        nuevo_usuario.save()
        nuevo_alumno.save()

        logging.info(funciones.obtener_ip_cliente(request) + ' ha registrado un alumno')
        messages.success(request, 'Alumno registrado exitosamente.')
        logging.info('%s ha registrado un usuario' % funciones.obtener_ip_cliente(request))
        return redirect('/')

    return render(request, "registro.html", {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

@funciones.logueado
def lista_ejercicios(request) -> HttpResponse:
    """Vista que regresa la página donde se mostrarán el listado de ejercicios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    if request.session['user_type'] == 'alumno':
        if request.method in ['GET', 'POST']:
            ejercicios = models.Ejercicio.objects.all()
            id_user = request.session['usuario']
            user = models.Usuario.objects.get(id=id_user)
            alumno = models.Alumno.objects.get(usuario=user)
            
            ejercicios_con_calificaciones = []
            for ejercicio in ejercicios:
                calificacion = models.Respuesta.objects.filter(ejercicio=ejercicio, alumno=alumno).first()
                calificacion_value = calificacion.calificacion if calificacion else "N/A"
                ejercicios_con_calificaciones.append((ejercicio, calificacion_value))

            logging.info('%s ha ingresado a la lista de ejercicios' % user.username)
            return render(request, "listaejercicios.html", {'ejercicios_con_calificaciones': ejercicios_con_calificaciones, 'usuario': user})
    else:
        return redirect('/verListaMaestro/')

@funciones.logueado
def definir_ejercicio(request) -> HttpResponse:
    """Vista con formulario para definición de ejercicio de programación

    Args:
        request (_type_): Petición

    Returns:
        HttpResponse: _description_
    """
    if request.session['user_type'] == 'profesor':
        if request.method == 'POST':

            nombre_ejercicio = request.POST.get('nombreEjercicio')
            descripcion_ejercicio = request.POST.get('descripcion')
            entrada1 = request.POST.get('entradaUno')
            entrada2 = request.POST.get('entradaDos')
            entrada3 = request.POST.get('entradaTres')
            salida1 = request.POST.get('salidaUno')
            salida2 = request.POST.get('salidaDos')
            salida3 = request.POST.get('salidaTres')
            fecha_inicio = request.POST.get('fechaInicio')
            fecha_cierre = request.POST.get('fechaCierre')
    
            ejercicio_nuevo = models.Ejercicio(
                nombre_ejercicio = nombre_ejercicio,
                descripcion = descripcion_ejercicio,
                valor = 3,
                entrada1 = entrada1,
                entrada2 = entrada2,
                entrada3 = entrada3,
                salida1 = salida1,
                salida2 = salida2,
                salida3 = salida3,
                fecha_inicio = fecha_inicio,
                fecha_cierre = fecha_cierre
            )
            ejercicio_nuevo.save()
            logging.info('El profesor ha ingresado creado nueva tarea')
            return redirect('/verListaMaestro/')
        return render (request, "subirEjercicioMaestro.html")
    else:
        return redirect('/lista/')


@funciones.logueado
def ver_ejercicio(request) -> HttpResponse:
    """Vista para visualizar el ejercio selecionado de la lista

    Args:
        request (_type_): Petición

    Returns:
        HttpResponse: Plantilla de verEjercicio.html
    """
    if request.session['user_type'] == 'profesor':
        if request.method == 'POST':
            id_ejercicio = request.POST.get('ejercicio_id')
            user_id = request.POST.get('user_id')

            usuario_id = request.session["usuario"]
            user = models.Usuario.objects.get(id=usuario_id)

            alumno = models.Alumno.objects.get(usuario = user)
            ejercicio_seleccionado = models.Ejercicio.objects.get(id=id_ejercicio)
            logging.info('El alumno %s ha ingresado al ejercicio %s' % (alumno.nombre, ejercicio_seleccionado.nombre_ejercicio))
            return render (request, "verEjercicio.html", {'ejercicio':ejercicio_seleccionado, 'usuario':user_id})
    else:
        return redirect('/verlistaMaestro/')

@funciones.notoken
def doble_factor(request) -> HttpResponse:
    """Vista para el ingreso del token doble factor, generando el objeto OTP, guardarlo en la base
    y al llenar el formulario se compara el token ingresado con el que ingresado en la base de datos,
    también compara el tiempo de vida del token, si alguno de estos dos falla se redirije al login, si
    es éxitoso redirije a la lista de tareas. 

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    if request.method == 'GET':
        usuario_id = request.session["usuario"]
        user = models.Usuario.objects.get(id=usuario_id)
        old_otps = models.UserOTP.objects.filter(usuario=user)#Eliminacion de OTPs antiguos del User
        old_otps.delete()
        otp = bot_tele.generate_otp()
        actual = datetime.now(timezone.utc)
        new_otp = models.UserOTP(ultimo_OTP=otp, fecha_ultimo_OTP=actual, usuario=user)
        new_otp.save()
        bot_tele.enviar_mensaje(otp, user) 
        logging.info('Se ha mandado token al bot de telegram')
        return render(request, "dobleFactor.html")
    if request.method == 'POST':
        usuario_id = request.session["usuario"]
        user = models.Usuario.objects.get(id=usuario_id)
        caracter1 = request.POST.get('character1')
        caracter2 = request.POST.get('character2')
        caracter3 = request.POST.get('character3')
        caracter4 = request.POST.get('character4')
        caracter5 = request.POST.get('character5')
        caracter6 = request.POST.get('character6')

        intento_otp = caracter1 + caracter2 + caracter3 + caracter4 + caracter5 + caracter6
        print(user.username)
        print(intento_otp)
        if funciones.validar_token(user, intento_otp):
            logging.info('%s se ha logeado éxitosamente con el usuario %s' % (funciones.obtener_ip_cliente(request), user.username))
            request.session["logueado"] = True
            request.session["notoken"] = False
            user_type = request.session.get('user_type')
            
            if user_type == 'alumno':
                return redirect('/lista/')
            elif user_type == 'profesor':
                return redirect('/verListaMaestro/')
        else:
            logging.error('%s ha ingresado incorrectamente el token para el usuario %s' % (funciones.obtener_ip_cliente(request), user.username))
            messages.error(request,'Token incorrecto o tiempo de token expirado')
            return redirect('/')
        
@funciones.logueado
def tarea_revisada(request) -> HttpResponse:
    """Vista encargada de tomar la respuesta del alumno y realizar el proceso de evaluación
    para posteriormente guardando en la base de datos

    Args:
        request (_type_): Petición

    Returns:
        HttpResponse: Respuesta HTTP
    """
    if request.session['user_type'] == 'profesor':
        if request.method == 'GET':
            return redirect('/lista/')
        if request.method == 'POST':
            id_ejercicio = request.POST.get('ejercicio_id')
            ejercicio_seleccionado = models.Ejercicio.objects.get(id=id_ejercicio)
            codigo = request.POST.get('codigo')
            user_id = request.session['usuario']
            usuario = models.Usuario.objects.get(id=user_id)
            alumno = models.Alumno.objects.get(usuario = usuario)

            respuesta_alumno = models.Respuesta(
                respuesta = codigo,
                calificacion = 0,
                ejercicio = ejercicio_seleccionado,
                alumno = alumno
            )

            calificacion_ejercicio = funciones.calificar_ejercicio(respuesta_alumno, ejercicio_seleccionado)

            respuesta_alumno.calificacion = calificacion_ejercicio
            respuesta_alumno.hora_entrega = datetime.now(timezone.utc)
            respuesta_alumno.save()
            logging.info('El alumno %s ha subido su respuesta al ejercicio %s' % (alumno.nombre, ejercicio_seleccionado.nombre_ejercicio))
            return redirect('/lista/')
    else:
        return redirect('/verListaMaestro/')

@funciones.logueado
def lista_ejercicio_maestro(request):
    if request.session['user_type'] == 'profesor':
        ejercicios = models.Ejercicio.objects.all()
        return render(request, "listaEjercicioMaestro.html", {'ejercicios':ejercicios})
    else:
        return redirect('/lista/')

@funciones.logueado
def tabla_ejerciciom(request):
    if request.session['user_type'] == 'profesor':
        ejercicios = models.Ejercicio.objects.all()
        ejercicios_con_respuesta = []
        for ejercicio in ejercicios:
            respuestas = models.Respuesta.objects.filter(ejercicio=ejercicio)
            ejercicios_con_respuesta.append((ejercicio, respuestas))
        return render(request,"tablaEjercicioMaestro.html", {'ejercicios_con_respuestas': ejercicios_con_respuesta})
    else:
        return redirect('/verListaMaestro/')

@funciones.logueado
def detalle_respuesta_maestro(request):
    if request.method == 'POST' and request.session.get('user_type') == 'profesor':
        respuesta_id = request.POST.get('respuesta_id')
        try:
            respuesta = models.Respuesta.objects.get(id=respuesta_id)
            return render(request, "detalleMaestro.html", {'respuesta': respuesta})
        except models.Respuesta.DoesNotExist:
            return redirect('/verListaMaestro/')
    else:
        return redirect('/verListaMaestro/')

def eliminar_ejercicio(request):
    if request.session['user_type'] == 'profesor':
        ejercicio_id = request.POST.get('ejercicio_id')
        ejercicio_seleccionado = models.Ejercicio.objects.get(id=ejercicio_id)

        ejercicio_seleccionado.delete()
        return redirect('/verListaMaestro/')
    else:
        return redirect('/lista/')

def logout(request) -> HttpResponse:
    """
    Función básica de logout.

    Keyword Arguments:
    request -- 
    returns: HttpResponse 
    """
    logging.info('El usuario cerro sesión')
    request.session.flush()
    return redirect('/')