from django.urls import path
from . import views

urlpatterns = [
    path('cronogramas/cronogramas-cursos/listar-cronogramas/', views.get, name='listar_cronogramas'),
    path('cronogramas/cronogramas-cursos/eliminar-cronogramas/', views.delete, name='eliminar_cronogramas'),
    path('cronogramas/cronogramas-cursos/detalles/curso/<str:curso_id>/mes/<str:mes_nombre>/', views.get_detalle_curso, name='get_detalle_curso'),
    ]