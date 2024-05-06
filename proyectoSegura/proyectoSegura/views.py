#Views.py

from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from db import models


def hello(request):
    return render(request, "login.html")

def registrarAlumno(request):
    return render(request, "registro.html")

def lista_ejercicios(request) -> HttpResponse:
    """Función que regresa la página donde se mostrarán el listado de ejercicios

    Args:
        request (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    return render(request, "listaejercicios.html")

#def login(request):
 #   return render(request, "login.html")
