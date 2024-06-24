"""
URL configuration for proyectoSegura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from proyectoSegura import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('registro/', views.registrar_alumno),
    path('lista/', views.lista_ejercicios),
    path('ejercicioMaestro/', views.definir_ejercicio),
    path('verEjercicio/', views.ver_ejercicio),
    path('doblefactor/', views.doble_factor),
    path("logout/", views.logout),
    path('captcha/', include('captcha.urls')),
    path("calificando/", views.tarea_revisada),
    #path("verEjericioMaestro/", views.verEjericio_Maestro),
    path("verListaMaestro/", views.lista_ejercicio_maestro),
    path("puntajeMaestro/", views.tabla_ejerciciom),
    path("detalleRespuesta/", views.detalle_respuesta_maestro),
    path("eliminarEjercicio/", views.eliminar_ejercicio),
    #path('login/', views.login),
]
