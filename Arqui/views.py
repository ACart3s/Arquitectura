from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Departamentos, Deuda, Boletapago
from datetime import datetime, timedelta
from django.db.models import Q

def generar_gastos_comunes(request, mes=None, anio=None):
    try:
        if mes and anio:  
            fecha_deuda = datetime(int(anio), int(mes), 1)
            for depto in departamentos.objects.all():
                
                deuda.objects.create(
                    monto=50000,  
                    fechaDeuda=fecha_deuda,
                    fechaVencimiento=fecha_deuda + timedelta(days=30),
                )
        elif anio:
            for mes in range(1, 13):
                fecha_deuda = datetime(int(anio), mes, 1)
                for depto in departamentos.objects.all():
                    deuda.objects.create(
                        monto=50000,  
                        fechaDeuda=fecha_deuda,
                        fechaVencimiento=fecha_deuda + timedelta(days=30),
                    )
        return JsonResponse({'status': 'Gastos comunes generados exitosamente'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})

def marcar_pago(request, depto_id, mes, anio):
    try:
        
        depto = departamentos.objects.get(idDepto=depto_id)

        boletapagos = Boletapago.objects.filter(
            depto__idDepto=depto_id,
            fechaPago__month=mes,
            fechaPago__year=anio
        )

        if boletapagos.exists():
            pagos = [
                {
                    "idPago": pago.idPago,
                    "monto": pago.monto.monto,
                    "fechaPago": pago.fechaPago,
                    "depto": pago.depto.numeroDepto
                }
                for pago in boletapagos
            ]
            return JsonResponse({"status": "Success", "pagos": pagos})
        else:
            return JsonResponse({"status": "Error", "message": "No se encontraron pagos para este mes y año"})
            #toy pa la caga chavales
    except departamentos.DoesNotExist:
        return JsonResponse({"status": "Error", "message": "Departamento no encontrado"})
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)})

def listar_pendientes(request, mes, anio):
    try:
        fecha_limite = datetime(int(anio), int(mes), 1)

        deudas_pendientes = deuda.objects.filter(
            fechaDeuda__lte=fecha_limite
        ).exclude(boletapago__isnull=False).order_by('fechaDeuda')

        if not deudas_pendientes.exists():
            return JsonResponse({'message': 'Sin montos pendientes'})

        resultado = []
        for deuda_obj in deudas_pendientes:
            resultado.append({
                'departamento': deuda_obj.depto.numeroDepto,
                'periodo': deuda_obj.fechaDeuda.strftime('%m/%Y'),
                'monto': deuda_obj.monto
            })

        return JsonResponse({'pendientes': resultado})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})

def listar_deudas_departamento(request, depto_id):
    try:
        departamento = departamentos.objects.get(idDepto=depto_id)
        deudas = deuda.objects.filter(idDepto=departamento)
        historial_deudas = []

        for d in deudas:
            pago = Boletapago.objects.filter(monto=d).first()
            estado_pago = "Pagado" if pago else "Pendiente"
            fecha_pago = pago.fechaPago if pago else None
            
            historial_deudas.append({
                "id_deuda": d.idDeuda,
                "monto": d.monto,
                "fecha_deuda": d.fechaDeuda,
                "fecha_vencimiento": d.fechaVencimiento,
                "estado_pago": estado_pago,
                "fecha_pago": fecha_pago
            })

        return JsonResponse({"departamento": departamento.numeroDepto, "historial_deudas": historial_deudas}, safe=False)

    except departamentos.DoesNotExist:
        return JsonResponse({"error": "Departamento no encontrado."}, status=404)

def reporte_pagos(request, mes, anio):
    pagos = Boletapago.objects.filter(fechaPago__month=mes, fechaPago__year=anio)
    reporte = []

    for p in pagos:
        reporte.append({
            "id_pago": p.idPago,
            "departamento": p.depto.numeroDepto,
            "monto_pagado": p.monto.monto,
            "fecha_pago": p.fechaPago
        })

    if not reporte:
        return JsonResponse({"mensaje": "No se encontraron pagos para el período especificado."}, safe=False)
    
    return JsonResponse({"reporte_pagos": reporte}, safe=False)

def notificar_deudas_vencidas(request):
    hoy = timezone.now().date()
    proximo_vencimiento = hoy + timedelta(days=7)

    deudas_vencidas = deuda.objects.filter(fechaVencimiento__lte=hoy, boletapago__isnull=True)
    deudas_proximas = deuda.objects.filter(fechaVencimiento__range=(hoy, proximo_vencimiento), boletapago__isnull=True)

    deudas_lista = []

    for d in deudas_vencidas:
        deudas_lista.append({
            "id_deuda": d.idDeuda,
            "departamento": d.idDepto.numeroDepto,
            "monto": d.monto,
            "fecha_vencimiento": d.fechaVencimiento,
            "estado": "Vencida"
        })

    for d in deudas_proximas:
        deudas_lista.append({
            "id_deuda": d.idDeuda,
            "departamento": d.idDepto.numeroDepto,
            "monto": d.monto,
            "fecha_vencimiento": d.fechaVencimiento,
            "estado": "Próxima a vencer"
        })

    if not deudas_lista:
        return JsonResponse({"mensaje": "No hay deudas vencidas o próximas a vencer."}, safe=False)

    return JsonResponse({"notificaciones": deudas_lista}, safe=False)


def historial_completo(request):
    departamentos_lista = departamentos.objects.all()
    historial = []

    for depto in departamentos_lista:
        deudas = deuda.objects.filter(idDepto=depto)
        deudas_info = []

        for d in deudas:
            pago = Boletapago.objects.filter(monto=d).first()
            estado_pago = "Pagado" if pago else "Pendiente"
            fecha_pago = pago.fechaPago if pago else None

            deudas_info.append({
                "id_deuda": d.idDeuda,
                "monto": d.monto,
                "fecha_deuda": d.fechaDeuda,
                "fecha_vencimiento": d.fechaVencimiento,
                "estado_pago": estado_pago,
                "fecha_pago": fecha_pago
            })

        historial.append({
            "departamento": depto.numeroDepto,
            "torre": depto.torre,
            "deudas": deudas_info
        })

    return JsonResponse({"historial": historial}, safe=False)
