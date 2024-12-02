from django.urls import path
from . import views

urlpatterns = [
    path('listar-cronogramas/', views.get, name='listar_cronogramas'),
    ]