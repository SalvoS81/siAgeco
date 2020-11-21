from django import forms

from ageco_db_manager.models import *

class TurnoProgrammatoForm(forms.ModelForm):  
    class Meta:
        model = TurnoProgrammato        
        fields = ['vettura', 'stato', 'sostituto', 'note']
        widgets = {
            'vettura': forms.Select(attrs={'class':'form-control'}),
            'stato': forms.Select(attrs={'class':'form-control'}),
            'sostituto': forms.Select(attrs={'class':'form-control'}),
            'note': forms.Textarea(attrs={'class':'form-control'}),
        }

class TurnoEffettivoForm(forms.ModelForm):  
    class Meta:
        model = TurnoEffettivo        
        fields = ['operatore', 'ora_inizio', 'ora_fine', 'polo_monta', 'polo_smonta', 'stato', 'note']
   
        widgets = {
            'operatore': forms.Select(attrs={'class':'form-control'}),
            'ora_inizio': forms.TimeInput(attrs={'class':'form-control'}),
            'ora_fine': forms.TimeInput(attrs={'class':'form-control'}),
            'polo_monta': forms.Select(attrs={'class':'form-control'}),
            'polo_smonta': forms.Select(attrs={'class':'form-control'}),
            'stato': forms.Select(attrs={'class':'form-control'}),            
            'note': forms.Textarea(attrs={'class':'form-control'}),
        }
        

class ScostamentoForm(forms.Form):
    scostamento = forms.IntegerField(label="Ore scostamento per simulazione", initial= 0, 
        max_value=12, min_value=-12,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )