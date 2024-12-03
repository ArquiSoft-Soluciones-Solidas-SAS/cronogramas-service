from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mongoengine import DoesNotExist

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
            "grado": cronograma.grado,
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

@csrf_exempt
def get_detalle_curso(request, curso_id, mes_nombre):
    """
    Obtiene los detalles del curso y mes especificado.
    """
    # Obtener todos los cronogramas que coinciden con el cursoId
    cronogramas = CronogramaBase.objects.filter(cursoId=curso_id)

    if cronogramas.count() == 0:
        return JsonResponse({"error": "Curso no encontrado"}, status=404)

    detalles = []
    for cronograma in cronogramas:
        for detalle in cronograma.detalle_cobro:
            if detalle.mes == mes_nombre:
                detalles.append({
                    "id": str(detalle.id),
                    "mes": detalle.mes,
                    "valor": str(detalle.valor),
                    "fechaCausacion": detalle.fechaCausacion,
                    "fechaLimite": detalle.fechaLimite,
                    "frecuencia": detalle.frecuencia
                })

    # Si no se encontraron detalles
    if not detalles:
        detalles.append({
            "mensaje": "No se encontraron detalles para el mes solicitado"
        })

    return JsonResponse({"detalles": detalles})


def get_all_detalles(request):
    """
    Obtiene todos los detalles de cobro.
    """
    cronogramas = CronogramaBase.objects.all()
    detalles = []
    for cronograma in cronogramas:
        for detalle in cronograma.detalle_cobro:
            detalles.append({
                "cursoId": str(cronograma.cursoId),
                "id": str(detalle.id),
                "mes": detalle.mes,
                "valor": str(detalle.valor),
                "fechaCausacion": detalle.fechaCausacion,
                "fechaLimite": detalle.fechaLimite,
                "frecuencia": detalle.frecuencia
            })

    return JsonResponse({"detalles": detalles})