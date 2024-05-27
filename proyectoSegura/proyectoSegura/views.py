#Views.py

from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db import models
from . import funciones


def login(request) -> HttpResponse:
    """Vista de logeo para usuarios, autentica profesores
    y alumnos en el mismo logeo

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    
    return render(request, "login.html")

def registrarAlumno(request) -> HttpResponse:
    """Vista para registro de usuarios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    return render(request, "registro.html")

def lista_ejercicios(request) -> HttpResponse:
    """Vista que regresa la página donde se mostrarán el listado de ejercicios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    return render(request, "listaejercicios.html")

#def login(request):
 #   return render(request, "login.html")
