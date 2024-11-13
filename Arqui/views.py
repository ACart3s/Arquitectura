from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Departamentos, Deuda, BoletaPago, DeptoHabitante
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
@csrf_exempt
def generar_gastos_comunes(request):
    mes = request.POST.get('mes')
    anio = request.POST.get('anio')
    print(mes, anio)
    try:
        if mes and anio:  
            fecha_deuda = datetime(int(anio), int(mes), 1)
            for depto in DeptoHabitante.objects.all():
                deuda = Deuda.objects.create(
                    monto=50000,  
                    fechaDeuda=fecha_deuda,
                    fechaVencimiento=fecha_deuda + timedelta(days=30),
                )

                boleta = BoletaPago.objects.create(
                    deuda=deuda,
                    depto=depto,
                )

                deuda.save()
                boleta.save()
        elif anio:
            for mes in range(1, 13):
                fecha_deuda = datetime(int(anio), mes, 1)
                for depto in DeptoHabitante.objects.all():
                    deuda = Deuda.objects.create(
                        monto=50000,  
                        fechaDeuda=fecha_deuda,
                        fechaVencimiento=fecha_deuda + timedelta(days=30),
                    )

                    boleta = BoletaPago.objects.create(
                        deuda=deuda,
                        depto=depto,
                    )

                    deuda.save()
                    boleta.save()
        return JsonResponse({'status': 'Gastos comunes generados exitosamente'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})

@require_POST
@csrf_exempt
def marcar_pago(request):
    depto_id = request.POST.get('depto_id')
    mes = request.POST.get('mes')
    anio = request.POST.get('anio')
    try:
        
        depto = Departamentos.objects.get(pk=depto_id)

        boletapagos = BoletaPago.objects.filter(
            depto=depto,
            fechaPago__month=mes,
            fechaPago__year=anio
        )

        if boletapagos.exists():
            pagos = [
                {
                    "idPago": pago.pk,
                    "monto": pago.deuda.monto,
                    "fechaPago": pago.fechaPago,
                    "depto": pago.depto.depto.numeroDepto
                }
                for pago in boletapagos
            ]
            return JsonResponse({"status": "Success", "pagos": pagos})
        else:
            return JsonResponse({"status": "Error", "message": "No se encontraron pagos para este mes y año"})
    except Departamentos.DoesNotExist:
        return JsonResponse({"status": "Error", "message": "Departamento no encontrado"})
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)})

@require_POST
@csrf_exempt
def listar_pendientes(request):
    mes = request.POST.get('mes')
    anio = request.POST.get('anio')
    try:

        fecha_limite = datetime(int(anio), int(mes), 1) + timedelta(days=30)

        deudas_pendientes = BoletaPago.objects.filter(
            deuda__fechaVencimiento__lte=fecha_limite,
            fechaPago__isnull=True,
            estado='N'
        )

        if not deudas_pendientes.exists():
            return JsonResponse({'message': 'Sin montos pendientes'})

        resultado = []
        for deuda_obj in deudas_pendientes:
            boleta = BoletaPago.objects.get(pk=deuda_obj.pk)
            resultado.append({
                'departamento': boleta.depto.depto.numeroDepto,
                'periodo': deuda_obj.deuda.fechaDeuda.strftime('%m/%Y'),
                'monto': deuda_obj.deuda.monto
            })

        return JsonResponse({'pendientes': resultado})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})