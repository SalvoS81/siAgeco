import django_filters
from django import forms
from ageco.settings import LANGUAGE_CODE
from datetime import date

from bootstrap_datepicker_plus import DateTimePickerInput

from ageco_db_manager.models import *

class FoglioServizioFilter(django_filters.FilterSet):
    #tipologia = django_filters.ChoiceFilter(choices=Nastro.TIPOLOGIA_OPZ, initial='Servizio',field_name='nastro__tipologia', label='Mansione',
    #    widget=forms.Select(attrs={'class':'form-control'})) # attrs={'style':'width:100%'}))  
    polo = django_filters.ChoiceFilter(choices=POLO_OPZ, field_name='nastro__polo_monta', label='Polo', 
        widget=forms.Select(attrs={'class':'form-control'})) # attrs={'style':'width:100%'}))
    data_servizio = django_filters.DateFilter(field_name='data', initial=date.today(),
        widget=DateTimePickerInput(format='%d/%m/%Y', attrs={'class':'form-control'},
            options={            
                    "locale": LANGUAGE_CODE,
                }))
    class Meta:
        model = TurnoProgrammato
        #fields = ['tipologia', 'polo', 'data_servizio',]
        fields = ['polo', 'data_servizio',]
    
    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)
    
def linee(request):
    if request is None:
        return Linea.objects.none()
    try:
        polo = request.GET['polo']
    except:
        return Linea.objects.all().filter(polo='R8')
    return Linea.objects.all().filter(polo=polo)

class GrigliaFilter(django_filters.FilterSet):
    polo = django_filters.ChoiceFilter(choices=POLO_OPZ, field_name='nastro__linea__polo', initial='R8', label='Polo',
        widget=forms.Select(attrs={'class':'form-control'})) #attrs={'style':'width:100%'})) 
    data_servizio = django_filters.DateFilter(field_name='data', initial=date.today(),
        widget=DateTimePickerInput(format='%d/%m/%Y', attrs={'class':'form-control'},
            options={            
                    "locale": LANGUAGE_CODE,
                }))
    linea = django_filters.ModelChoiceFilter(queryset=linee, field_name='nastro__linea', label='Linea',
        widget=forms.Select(attrs={'class':'form-control'})) #attrs={'style':'width:100%'}))

    class Meta:
        model = TurnoProgrammato
        fields = ['polo', 'data', 'linea']  
      
    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)

class AssenzeFilter(django_filters.FilterSet):    
    data_servizio = django_filters.DateFilter(field_name='data', initial=date.today(),
        widget=DateTimePickerInput(format='%d/%m/%Y', attrs={'class':'form-control'},
            options={            
                    "locale": LANGUAGE_CODE,
                }))
    class Meta:
        model = TurnoEffettivo
        fields = ['data']  
      
    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)