from django.urls import path
from . import views

urlpatterns = [
    path('cronogramas/cronogramas-cursos/listar-cronogramas/', views.get, name='listar_cronogramas'),
    path('cronogramas/cronogramas-cursos/eliminar-cronogramas/', views.delete, name='eliminar_cronogramas'),
    ]