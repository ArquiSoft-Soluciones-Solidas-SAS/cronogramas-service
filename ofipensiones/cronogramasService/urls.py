from django.urls import path
from . import views

urlpatterns = [
    path('cronogramas/cronogramas-cursos/listar-cronogramas/', views.get, name='listar_cronogramas'),
    ]