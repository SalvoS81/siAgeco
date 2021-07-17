from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from ageco_db_manager.models import *
from .forms import *
from .filters import *

import datetime


def is_193(user):
    return user.groups.filter(name='Addetti Esercizio').exists()

def is_oe(user):
    return user.groups.filter(name='Operatori Esercizio').exists()

@login_required
@user_passes_test(is_193)
def foglio_servizio(request):
    if not request.GET:
        request.GET = request.GET.copy()
        if 'polo' in request.session:
            polo = request.session['polo']
            request.GET['polo'] = polo
        if 'tipologia' in request.session:
            tipologia = request.session['tipologia']
            request.GET['tipologia'] = tipologia
        if 'data_servizio' in request.session:
            data_servizio = request.session['data_servizio']
            request.GET['data_servizio'] = data_servizio
        if 'scostamento' in request.session:    #test
            scostamento = request.session['scostamento']
            request.GET['scostamento'] = scostamento
     
    request.session['polo'] = request.GET.get('polo',"")
    request.session['tipologia'] = request.GET.get('tipologia',"")
    request.session['data_servizio'] = request.GET.get('data_servizio',"")
    request.session['scostamento'] = request.GET.get('scostamento', 0)  #test

    turni_list = TurnoProgrammato.objects.all().order_by('nastro__ora_inizio')
    turni_filter = FoglioServizioFilter(request.GET, request=request, queryset=turni_list)
    riserve = turni_filter.qs.filter(Q(nastro__tipologia='Riserva') | Q(stato__stato='Inoperoso'))
    servizio = turni_filter.qs.filter(nastro__tipologia='Servizio')
    form_scostamento = ScostamentoForm(request.GET)
    return render(request, 'vista/foglio_servizio.html', {'filter': turni_filter, 'servizio': servizio, 'riserve': riserve, 'form_scostamento': form_scostamento})

@login_required
@user_passes_test(is_193)
def griglia_polo(request):
    if not request.GET:
        request.GET = request.GET.copy()
        if 'polo' in request.session:
            polo = request.session['polo']
            request.GET['polo'] = polo
        if 'linea' in request.session:
            linea = request.session['linea']
            request.GET['linea'] = linea
        if 'data_servizio' in request.session:
            data_servizio = request.session['data_servizio']
            request.GET['data_servizio'] = data_servizio
    
     
    request.session['polo'] = request.GET.get('polo',"")
    request.session['linea'] = request.GET.get('linea',"")
    request.session['data_servizio'] = request.GET.get('data_servizio',"")
    
    griglia_list = TurnoProgrammato.objects.all().filter(nastro__tipologia='Servizio').order_by('nastro__linea', 'nastro__treno' , 'nastro__ora_inizio')
    griglia_filter = GrigliaFilter(request.GET, request=request, queryset=griglia_list)

    data = datetime.datetime.strptime(request.session['data_servizio'], '%d/%m/%Y')
    turnieffettivi_list = TurnoEffettivo.objects.all().filter(Q(data=data) | Q(linea__polo=request.session['polo'])).order_by('linea', 'treno' , 'ora_inizio') #| Q(linea=request.session['linea']))
    
    return render(request, 'vista/griglia_polo.html', {'filter': griglia_filter, 'turnieffettivi': turnieffettivi_list})

class TurnoProgrammatoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TurnoProgrammato
    form_class = TurnoProgrammatoForm
    #fields = ['vettura', 'stato', 'sostituto', 'note']
    template_name = "ageco_db_manager/turnoprogrammato_form.html"

    def test_func(self):
        return self.request.user.groups.filter(name='Addetti Esercizio').exists()

    def get_context_data(self, **kwargs):
        context = super(TurnoProgrammatoUpdateView, self).get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next') # pass `next` parameter received from previous page to the context 
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url # return next url for redirection
        return reverse('home') # return some other url if next parameter not present

class TurnoEffettivoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TurnoEffettivo
    form_class = TurnoEffettivoForm    
    template_name = "ageco_db_manager/turnoeffettivo_form.html"

    def test_func(self):
        return self.request.user.groups.filter(name='Addetti Esercizio').exists()

    def get_context_data(self, **kwargs):
        context = super(TurnoEffettivoUpdateView, self).get_context_data(**kwargs)
        context['next_url'] = self.request.GET.get('next') # pass `next` parameter received from previous page to the context 
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url # return next url for redirection
        return reverse('home') # return some other url if next parameter not present

@login_required
@user_passes_test(is_193)
def report_assenze(request):
    if not request.GET:
        request.GET = request.GET.copy()        
        if 'data_servizio' in request.session:
            data_servizio = request.session['data_servizio']
            request.GET['data_servizio'] = data_servizio
    
        
    request.session['data_servizio'] = request.GET.get('data_servizio',"")
    
    data = datetime.datetime.strptime(request.session['data_servizio'], '%d/%m/%Y')
    assenze_list = TurnoProgrammato.objects.all().filter(Q(data=data), Q(stato='7') | Q(stato='8'))
    assenze_filter = AssenzeFilter(request.GET, request=request, queryset=assenze_list)
   
    return render(request, 'vista/report_assenze.html', {'filter': assenze_filter, })