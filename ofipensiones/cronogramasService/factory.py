from datetime import date, timedelta

from bson import ObjectId
from factory.mongoengine import MongoEngineFactory
from mongoengine import DoesNotExist

from .models import CronogramaBase, DetalleCobroCurso
import factory
from django.conf import settings
import requests
import json
import random

class CronogramaBaseFactory(MongoEngineFactory):
    class Meta:
        model = CronogramaBase

cursosGlobales = []
def obtener_cursos_embebidos():
    """
    Conecta a la base de datos remota y obtiene los cursos embebidos dentro de las instituciones.
    """
    r = requests.get(settings.PATH_INSTITUCIONES + "/listar-instituciones/", headers={"Accept":"application/json"})
    if r.status_code != 200:
        print("Error al obtener las instituciones.")
        return []
    instituciones = r.json()["instituciones"]
    print("Instituciones obtenidas exitosamente.")
    print("Instituciones: ", instituciones)
    for institucion in instituciones:
        for curso in institucion["cursos"]:
            cursosGlobales.append({
                "id": curso["id"],
                "nombreInstitucion": institucion["nombreInstitucion"],
                "institucionEstudianteId": institucion["id"],
                "grado": curso["grado"]
            })
    return cursosGlobales

def crear_cronogramas_bases():
    cursos = obtener_cursos_embebidos()  # Obtener todos los cursos
    for curso in cursos:
        crear_cronogramas_para_curso(curso)

def crear_cronogramas_para_curso(curso):
    # Crear cronograma para matrícula
    CronogramaBaseFactory(institucionId=curso["institucionEstudianteId"],
                          nombreInstitucion=curso["nombreInstitucion"],
                          cursoId=curso["id"],
                          codigo=f"M-{curso['id']}",
                          nombre="Matrícula anual")

    CronogramaBaseFactory(institucionId=curso["institucionEstudianteId"],
                          nombreInstitucion=curso["nombreInstitucion"],
                          cursoId=curso["id"],
                          codigo=f"P-{curso['id']}",
                          nombre="Pensión mensual")

    # Crear cronograma para inglés (opcional)
    if random.choice([True, False]):  # Aproximadamente 50% de probabilidades de tener inglés
        CronogramaBaseFactory(institucionId=curso["institucionEstudianteId"],
                              nombreInstitucion=curso["nombreInstitucion"],
                              cursoId=curso["id"],
                              codigo=f"I-{curso['id']}",
                              nombre="Curso de inglés")


def generar_detalles_cobro_para_instituciones():
    global curso
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
             'Noviembre', 'Diciembre']
    grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno',
              'Décimo', 'Undécimo']
    print(cursosGlobales)
    for cronograma in CronogramaBase.objects.all():
        # Obtener información del curso correspondiente
        for curso in cursosGlobales:
            print("curso actual: ", curso)
            if curso["id"] == cronograma.cursoId:
                break
            else:
                curso = None

        if curso is None:
            print(f"Curso no encontrado: {cronograma.cursoId}")
            continue

        # Calcular el factor según el grado del curso
        factor_grado = (grados.index(curso["grado"]) + 1) / len(grados)
        pension_base = random.randint(100000, 250000) * factor_grado
        multiplicador_matricula = random.uniform(4, 6)

        # Crear detalles específicos por tipo de cronograma
        detalles = []
        if cronograma.nombre == "Matrícula anual":
            valor = pension_base * multiplicador_matricula
            fecha_causacion = date.today().replace(month=1, day=1)
            fecha_limite = fecha_causacion + timedelta(weeks=3)
            detalle = DetalleCobroCurso(
                id=ObjectId(),
                mes="Enero",
                valor=valor,
                fechaCausacion=fecha_causacion,
                fechaLimite=fecha_limite,
                frecuencia="Anual"
            )
            detalles.append(detalle)

        elif cronograma.nombre == "Pensión mensual":
            for i, mes in enumerate(meses):
                if mes != "Enero":
                    valor = pension_base
                    fecha_causacion = date.today().replace(month=i + 1, day=1)
                    fecha_limite = fecha_causacion + timedelta(days=15)
                    detalle = DetalleCobroCurso(
                        id=ObjectId(),
                        mes=mes,
                        valor=valor,
                        fechaCausacion=fecha_causacion,
                        fechaLimite=fecha_limite,
                        frecuencia="Mensual"
                    )
                    detalles.append(detalle)

        elif cronograma.nombre == "Curso de inglés":
            valor = 200000
            fecha_causacion = date.today().replace(month=1, day=1)
            fecha_limite = fecha_causacion + timedelta(weeks=2)
            detalle = DetalleCobroCurso(
                id=ObjectId(),
                mes="Enero",
                valor=valor,
                fechaCausacion=fecha_causacion,
                fechaLimite=fecha_limite,
                frecuencia="Anual"
            )
            detalles.append(detalle)

        # Actualizar el cronograma con los detalles generados
        try:
            cronograma.update(push_all__detalle_cobro=detalles)
            print(f"Detalles añadidos al cronograma: {cronograma.codigo}")
        except DoesNotExist:
            print(f"Error al actualizar cronograma: {cronograma.codigo}")