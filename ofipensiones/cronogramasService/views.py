from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CronogramaBase


@csrf_exempt
def get(request):
    cronogramas = CronogramaBase.objects.all()
    resultado = []
    for cronograma in cronogramas:
        resultado.append({
            "id": str(cronograma.id),
            "nombreInstitucion": cronograma.nombreInstitucion,
            "cursoId": str(cronograma.cursoId),
            "codigo": cronograma.codigo,
            "nombre": cronograma.nombre,
            "detalle_cobro": [
                {
                    "id": str(detalle.id),
                    "mes": detalle.mes,
                    "valor": str(detalle.valor),
                    "fechaCausacion": detalle.fechaCausacion,
                    "fechaLimite": detalle.fechaLimite,
                    "frecuencia": detalle.frecuencia
                }
                for detalle in cronograma.detalle_cobro
            ]
        })
    return JsonResponse({"cronogramas": resultado})

@csrf_exempt
def delete(request):
    cronogramas = CronogramaBase.objects.all()
    for cronograma in cronogramas:
        cronograma.delete()
    return JsonResponse({"mensaje": "Cronogramas eliminados"})