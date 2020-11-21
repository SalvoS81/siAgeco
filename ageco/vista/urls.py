from django.urls import path
from django.views.generic.base import TemplateView
#from django_filters.views import FilterView
#from .filters import MonteFilter
import vista.views as views

urlpatterns = [
    path('', TemplateView.as_view(template_name='vista/home.html'), name='home'),
    path('foglio_servizio/', views.foglio_servizio, name='foglio_servizio'),
    path('griglia_polo/', views.griglia_polo, name='griglia_polo'),
    path('report_assenze/', views.report_assenze, name='report_assenze'),
    path('turno_programmato/<int:pk>/update/', views.TurnoProgrammatoUpdateView.as_view(), name='turno_programmato_update'),
    path('turno_effettivo/<int:pk>/update/', views.TurnoEffettivoUpdateView.as_view(), name='turno_effettivo_update'),
]