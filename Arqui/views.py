from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import departamentos, deuda, Boletapago
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
        #que pasa si les dejo un comentario aqui lo leen o no muchachos diganme que pasa porfa
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


