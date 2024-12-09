from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Departamentos, Deuda, BoletaPago, DeptoHabitante
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import LoginForm
from django.http import Http404

@login_required(login_url='/login/')
def index(request):
    return render(request, 'Arqui/index.html')

@login_required(login_url='/login/')
def generator(request):
    return render(request, 'Arqui/generator.html')

@login_required(login_url='/login/')
def pending(request):
    return render(request, 'Arqui/pending.html')

@login_required(login_url='/login/')
def checkPayment(request):
    return render(request, 'Arqui/check.html')

def login(request):

    if request.user.is_authenticated:
            raise Http404

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                auth_login(request, user)
                
                next = request.GET.get("next")
                if next != '' and next is not None:
                    return redirect(next)
                
                return redirect ('index')
            else:
                messages.error(request, "Email o Contraseña incorrectos")
                return redirect('login')
        else:
            messages.error(request, "Email o Contraseña incorrectos")
            return redirect('login')

    return render(request, 'Arqui/login.html')

@require_POST
def generar_gastos_comunes(request):
    monto = request.POST.get('monto')
    mes = request.POST.get('mes')
    anio = request.POST.get('anio')
    generated = []
    try:
        if mes and anio:  
            fecha_deuda = datetime(int(anio), int(mes), 1)
            for depto in DeptoHabitante.objects.all():
                deuda = Deuda.objects.create(
                    monto=monto,  
                    fechaDeuda=fecha_deuda,
                    fechaVencimiento=fecha_deuda + timedelta(days=30),
                )

                boleta = BoletaPago.objects.create(
                    deuda=deuda,
                    depto=depto,
                )

                generated.append({
                    'monto': monto,
                    'depto': depto.depto.numeroDepto,
                    'fechaDeuda': fecha_deuda.date(),
                })

                deuda.save()
                boleta.save()
            return JsonResponse({'complete': True, 'status': 'Gastos comunes generados exitosamente', 'generated': generated})
        elif anio:
            for mes in range(1, 13):
                fecha_deuda = datetime(int(anio), mes, 1)
                for depto in DeptoHabitante.objects.all():
                    deuda = Deuda.objects.create(
                        monto=monto,  
                        fechaDeuda=fecha_deuda,
                        fechaVencimiento=fecha_deuda + timedelta(days=30),
                    )

                    boleta = BoletaPago.objects.create(
                        deuda=deuda,
                        depto=depto,
                    )

                    generated.append({
                        'monto': monto,
                        'depto': depto.depto.numeroDepto,
                        'fechaDeuda': fecha_deuda,
                    })

                    deuda.save()
                    boleta.save()
            return JsonResponse({'complete': True, 'status': 'Gastos comunes generados exitosamente', 'generated': generated})
        else:
            return JsonResponse({'complete': False, 'status': 'Error', 'message': 'Falta mes y año'})
    except Exception as e:
        return JsonResponse({'complete': False,'status': 'Error', 'message': str(e)})

@require_POST
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
            return JsonResponse({'complete': True, "status": "Success", "pagos": pagos})
        else:
            return JsonResponse({'complete': False ,"status": "Error", "message": "No se encontraron pagos para este mes y año"})
    except Departamentos.DoesNotExist:
        return JsonResponse({'complete': True, "status": "Error", "message": "Departamento no encontrado"})
    except Exception as e:
        return JsonResponse({'complete': True, "status": "Error", "message": str(e)})

@require_POST
def listar_pendientes(request):
    mes = request.POST.get('mes')
    anio = request.POST.get('anio')

    try:

        fecha_limite = datetime(int(anio), int(mes), 1) + timedelta(days=30)
        fecha_inicio = datetime(int(anio), int(mes), 1)

        deudas_pendientes = BoletaPago.objects.filter(
            deuda__fechaVencimiento__lte=fecha_limite,
            deuda__fechaVencimiento__gte=fecha_inicio,
            fechaPago__isnull=True,
            estado='N'
        )

        if not deudas_pendientes.exists():
            return JsonResponse({'complete': False, 'message': 'Sin montos pendientes'})

        resultado = []
        for deuda_obj in deudas_pendientes:
            boleta = BoletaPago.objects.get(pk=deuda_obj.pk)
            resultado.append({
                'id': boleta.pk,
                'departamento': boleta.depto.depto.numeroDepto,
                'periodo': deuda_obj.deuda.fechaDeuda.strftime('%m/%Y'),
                'monto': deuda_obj.deuda.monto
            })

        return JsonResponse({'complete': True, 'pendientes': resultado})
    except Exception as e:
        return JsonResponse({'complete': False, 'status': 'Error', 'message': str(e)})


@require_POST
def pago_realizado(request):
    mes = request.POST.get('mes')
    anio = request.POST.get('anio')
    departamento = request.POST.get('departament')

    if not mes or not anio:
        return JsonResponse({'complete': False, 'status': 'Error', 'message': 'Falta mes y año'})
    try:
        pago = BoletaPago.objects.get(
            depto__depto__numeroDepto=departamento,
            deuda__fechaDeuda__month=mes,
            deuda__fechaDeuda__year=anio
        )

        if (pago.estado == 'P'):
            return JsonResponse({'complete': False, 'status': 'Error', 'message': 'Pago ya realizado'})
        
        pago.fechaPago = datetime.now()
        pago.estado = 'P'
        pago.save()
        return JsonResponse({'complete': True, 'status': 'Pago realizado exitosamente'})
    except BoletaPago.DoesNotExist:
        return JsonResponse({'complete': False,'status': 'Error', 'message': 'Pago no encontrado'})
    except Exception as e:
        return JsonResponse({'complete': False, 'status': 'Error', 'message': str(e)})