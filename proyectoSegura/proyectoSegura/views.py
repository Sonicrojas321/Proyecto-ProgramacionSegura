#Views.py
from django.contrib import messages
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db import models
from proyectoSegura import settings
from . import funciones, bot_tele


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
                #Usuario autenticado
                request.session['usuario'] = user.id
                print('logeado')
                redirect('/doblefactor/')
            else:
                error = 'Credenciales inválidas'
                return render(request, 'login.html', {'errores': error})

        except models.Usuario.DoesNotExist:
            error = 'Credenciales inválidas'
            return render(request, 'login.html', {'errores': error})
    

def registrar_alumno(request) -> HttpResponse:
    """Vista para registro de usuarios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombreAlumno')
        apellidos = request.POST.get('apellidosAlumno')
        usuario = request.POST.get('usuarioAlumno')
        contrasena = request.POST.get('contrasenaAlumno')
        confirm_contrasena = request.POST.get('contrasenaAlumno1')
        if contrasena == confirm_contrasena:
            contrasena = funciones.crear_password_hasheada(contrasena)
            nuevo_usuario = models.Usuario(
                username=usuario,
                password=contrasena
            )
            nuevo_alumno = models.Alumno(
                nombre = nombre,
                apellido = apellidos,
                usuario = nuevo_usuario
            )
            nuevo_usuario.save()
            nuevo_alumno.save()
            return redirect('/')

    return render(request, "registro.html")

def lista_ejercicios(request) -> HttpResponse:
    """Vista que regresa la página donde se mostrarán el listado de ejercicios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    ejercicios = models.Ejercicio.objects.all()
    return render(request, "listaejercicios.html", {'ejercicios':ejercicios})

def definir_ejercicio(request) -> HttpResponse:
    """Vista con formulario para definición de ejercicio de programación

    Args:
        request (_type_): Petición

    Returns:
        HttpResponse: _description_
    """
    if request.method == 'POST':
        nombre_ejercicio = request.POST.get('nombreEjercicio')
        descripcion_ejercicio = request.POST.get('descripcion')
        entrada1 = request.POST.get('entradaUno')
        entrada2 = request.POST.get('entradaDos')
        entrada3 = request.POST.get('entradaTres')
        salida1 = request.POST.get('salidaUno')
        salida2 = request.POST.get('salidaDos')
        salida3 = request.POST.get('salidaTres')

        ejercicio_nuevo = models.Ejercicio(
            nombre_ejercicio = nombre_ejercicio,
            descripcion = descripcion_ejercicio,
            valor = 3,
            entrada1 = entrada1,
            entrada2 = entrada2,
            entrada3 = entrada3,
            salida1 = salida1,
            salida2 = salida2,
            salida3 = salida3
        )
        ejercicio_nuevo.save()
        return redirect('/lista/')
    return render (request, "subirEjercicioMaestro.html")

def ver_ejercicio(request) -> HttpResponse:
    if request.method == 'POST':
        id_ejercicio = request.POST.get('ejercicio_id')
        print(id_ejercicio)
        ejercicio_seleccionado = models.Ejercicio.objects.get(id=id_ejercicio)
        return render (request, "verEjercicio.html", {'ejercicio':ejercicio_seleccionado})
    return render(request, "verEjercicio.html")

#@funciones.logueado
def doble_factor(request) -> HttpResponse:
    if request.method == 'GET':
        usuario_id = request.session["usuario"]
        bot_tele.generate_otp()
        return render(request, "dobleFactor.html")
    if request.method == 'POST':
        caracter1 = request.POST.get('character1')
        caracter2 = request.POST.get('character2')
        caracter3 = request.POST.get('character3')
        caracter4 = request.POST.get('character4')
        caracter5 = request.POST.get('character5')
        caracter6 = request.POST.get('character6')
        
    


def logout(request) -> HttpResponse:
    """
    Función básica de logout.

    Keyword Arguments:
    request -- 
    returns: HttpResponse 
    """
    request.session.flush()
    return redirect('/')