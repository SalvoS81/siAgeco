from django.template.defaulttags import register
from datetime import datetime

@register.filter
def get_item(value, chiave):
    for coppia in value:
        if chiave in coppia: return coppia[1]
    return None

@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica se esiste un gruppo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.filter('is_addetto_esercizio')
def is_addetto_esercizio(user):    
    return has_group(user, "Addetti Esercizio")

@register.filter('is_operatore_esercizio')
def is_addetto_esercizio(user):    
    return has_group(user, "Operatori Esercizio")

@register.filter('str_to_data')
def str_to_data(value):
    return datetime.strptime(value, '%d/%m/%Y').date()