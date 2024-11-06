"""
URL configuration for Arquitectura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Arqui import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generar_gastos/<int:mes>/<int:anio>/', views.generar_gastos_comunes, name='generar_gastos_comunes'),
    path('marcar_pago/<int:depto_id>/<int:mes>/<int:anio>/', views.marcar_pago, name='marcar_pago'),
    path('listar_pendientes/<int:mes>/<int:anio>/', views.listar_pendientes, name='listar_pendientes'),
]