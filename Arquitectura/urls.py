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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #EndPoints
    path('generar_gastos/', views.generar_gastos_comunes, name='generar_gastos_comunes'),
    path('marcar_pago/', views.marcar_pago, name='marcar_pago'),
    path('listar_pendientes/', views.listar_pendientes, name='listar_pendientes'),
    path('realizar_pago/', views.pago_realizado, name='pagar'),


    #FrontEnd
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('generator/', views.generator, name='generator'),
    path('pending/', views.pending, name='pending'),
    path('pay/', views.checkPayment, name='pay'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
