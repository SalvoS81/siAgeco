from django.db import models
from django import forms

from django.contrib.auth.models import User
from datetime import date
#from django.utils import timezone
from django.urls import reverse  # To generate URLS by reversing URL patterns
#from django.utils.translation import gettext_lazy as _
from django.template import defaultfilters
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import DEFERRED, Q   # used into from_db

import logging
logger = logging.getLogger(__name__)

POLO_OPZ = (
        ('R1','Rimessa 1'),
        ('R8','Rimessa 8'),
        ('AL','P.za Borsellino'),
        ('ST','Stazione Centrale'),
        ('RP','P.za Repubblica'),
        ('PB','P.za Borsa'),
        ('SZ','P.za Sanzio'),
        ('OB','Due Obelischi'),
        ('NE','Nesima'),
        ('FN','Fontanarossa'),
        ('VA','Villaggio S\'Agata'),)

class Persona(models.Model):    
    cognome = models.CharField(max_length=50)  
    nome = models.CharField(max_length=50)  
    data_di_nascita = models.DateField(blank=True, null=True)  
    paese_di_nascita = models.CharField(max_length=50, blank=True, null=True)  
    comune_di_nascita = models.CharField(max_length=50, blank=True, null=True)  
    
    SESSO_OPZ = ( 
        ('M', 'maschile'), 
        ('F', 'femminile'), 
    )

    sesso = models.CharField(
        max_length=1,
        blank=True, 
        null=True,
        choices=SESSO_OPZ,
        default='M',)  

    users = models.ManyToManyField(
        User, 
        limit_choices_to={'is_staff': False},
        help_text="Associa uno o più utenti a questa persona.",
        blank=True, 
        verbose_name='Utenti associati')
    
    class Meta:
        verbose_name_plural="Persone"
    
    def display_users(self):        
        return ', '.join([user.username for user in self.users.all()[:3]])

    display_users.short_description = 'Utenti associati'

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)

class Operatore(models.Model):
    identificativo = models.CharField(unique=True, max_length=20)
    matricola = models.CharField(unique=True, max_length=5, blank=True, null=True)
    pin = models.CharField(max_length=6, blank=True, null=True)    
    data_inquadramento= models.DateField(editable=True, blank=True, null=True)
    class Parametro(models.IntegerChoices):
        _140 = 140
        _158 = 158
        _175 = 175
        _183 = 183
        _193 = 193
    parametro = models.IntegerField(blank=True, null=True, choices= Parametro.choices,)
    #sequenzeRiposi
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural="Operatori"
        ordering=['identificativo']

    def __str__(self):
        return self.identificativo

class Linea(models.Model):
    nome = models.CharField(primary_key=True, unique=True, max_length=5)      
    polo = models.CharField( 
        max_length=2,
        blank=True, 
        null=True,
        default='R8',
        choices=POLO_OPZ,)
    descrizione = models.CharField(max_length=255, blank=True, null=True)  
    percorso = models.CharField(max_length=255, blank=True, null=True)  
    class Meta:
        verbose_name_plural="Linee"
        ordering=['nome']

    def __str__(self):
        return self.nome

class Nastro(models.Model): 
    empty_value_display = '---'
    linea = models.ForeignKey(Linea, to_field='nome', on_delete=models.SET_NULL, blank=True, null=True)
    treno = models.CharField(max_length=4, blank=True, null=True)
    TIPOLOGIA_OPZ = (('Servizio', 'Servizio'), ('Riserva', 'Riserva'),('Verifica', 'Verifica'))
    tipologia = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        choices=TIPOLOGIA_OPZ)
    FASCIA_OPZ = (('M', 'Mattinale'), ('S', 'Serale'),)
    fascia = models.CharField( 
        max_length=1,
        blank=True, 
        null=True,
        choices=FASCIA_OPZ,)
    ora_inizio = models.TimeField()
    ora_fine = models.TimeField()    
    polo_monta = models.CharField( 
        max_length=2,
        blank=True, 
        null=True,
        choices=POLO_OPZ,)
    polo_smonta = models.CharField( 
        max_length=2,
        blank=True, 
        null=True,
        choices=POLO_OPZ,)
 
    seguente = models.OneToOneField('self', models.SET_NULL, blank=True, null=True, related_name='seguente_di')# ,limit_choices_to = Q(precedente = None))
    precedente = models.OneToOneField('self', models.SET_NULL,   blank=True, null=True, related_name='precedente_di') #,limit_choices_to=Q(seguente = None))
    
    periodo_di_validita = models.CharField(max_length = 50, blank=True, null=True)

    class Meta:
        verbose_name_plural="Nastri"
        ordering = ['tipologia', 'ora_inizio']
        constraints = [
            models.UniqueConstraint(fields=['tipologia', 'linea', 'ora_inizio', 'ora_fine', 'polo_monta', 'periodo_di_validita'], name='unique_nastro')
        ]    

    def foglio(self):
        if self.tipologia == 'Servizio':
            return ('%s/%s' % (self.linea, self.treno))
        if self.tipologia == 'Riserva':
            return ('%s %s %s' % (self.tipologia, self.ora_inizio.strftime("%H:%M"), self.polo_monta))
        else:
            return ('%s %s' % (self.tipologia, self.ora_inizio.strftime("%H:%M")))
    foglio.short_description = 'Foglio'

    def formated_foglio(self):
        foglio = ''
        if self.tipologia == 'Servizio':
            foglio = ('%s/%s' % (self.linea, self.treno))
        elif self.tipologia == 'Riserva':
            foglio = ('%s %s %s' % (self.tipologia, self.ora_inizio.strftime("%H:%M"), self.polo_monta))
        else:
            foglio = ('%s %s' % (self.tipologia, self.ora_inizio.strftime("%H:%M")))        
        return format_html('<strong> {} </strong> ({} | {} - {} {}) ', foglio, self.ora_inizio.strftime("%H:%M"), self.ora_fine.strftime("%H:%M"), self.polo_monta, self.polo_smonta)

    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        if len(values) != len(cls._meta.concrete_fields):
            values = list(values)
            values.reverse()
            values = [
                values.pop() if f.attname in field_names else DEFERRED
                for f in cls._meta.concrete_fields
            ]
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, aggiornaParenti = True, *args, **kwargs):    #aggiorna precedente o seguente 
        #do_something()
        #super().save(*args, **kwargs)  # Call the "real" save() method.
        #do_something_else()

        #LOGGING CALL *********************
        logger.debug('Save - AggiornaParenti >> %s' % (aggiornaParenti))
        for i in args:
            logger.debug('Save - args >> %s' % i)
        for i in kwargs:
            logger.debug('Save - args >> %s' % i)
        logger.debug('Save - self ------------ [[[ %s ]]] ------------' % self)
        logger.debug('Save - self >> p: %s | s: %s' % (self.precedente, self.seguente))
        if self.seguente is not None: 
            s = self.seguente.precedente
            logger.debug('Save - il precedente di %s è %s ' % ( self.seguente, s ))
        if self.precedente is not None: 
            p = self.precedente.seguente
            logger.debug('Save - il seguente di %s è %s' % ( self.precedente, p))         
        
        #LOGICA 
        # TODO: aggiornare collegamenti
        
        if not self._state.adding and aggiornaParenti: # se il record non è nuovo recupera i vecchio valori
            vp = vs = None
            logger.debug('Save - Record in aggiornamento. Carico vecchi collegamenti.')
            vp = self._loaded_values['precedente_id']
            vs = self._loaded_values['seguente_id']
            logger.debug('Save - self _loaded_values >> %s' % self._loaded_values)
            logger.debug('Save - self _loaded_values >> vs: %s | vp: %s' % ( vs, vp))
            if self.precedente_id != vp and vp is not None:
                logger.debug('Save - precedente_id  >> Cambiato' )
                #vp->s = None save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vp)
                logger.debug('Save - obj.s >> %s' % obj.seguente )
                obj.seguente = None
                obj.save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vp) 
                logger.debug('Save - obj.s >> %s' % obj.seguente )             
            if self.seguente_id != vs and vs is not None:
                logger.debug('Save - seguente_id  >> Cambiato' )
                #vs->p = None save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vs)
                logger.debug('Save - obj.p >> %s' % obj.precedente )
                obj.precedente = None
                obj.save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vs) # solo per debug
                logger.debug('Save - obj.p >> %s' % obj.precedente )
                
        if self.precedente is not None and aggiornaParenti:
            logger.debug('Save - precedente is not None' )
            self.precedente.seguente = self
            self.precedente.save(aggiornaParenti = False)
        if self.seguente is not None and aggiornaParenti:
            logger.debug('Save - seguente is not None' )
            self.seguente.precedente = self
            self.seguente.save(aggiornaParenti = False)
        
        #super(Nastro, self).save(*args, **kwargs)
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def get_absolute_url(self):        
        logger.debug('absolute!')
        """Returns the url to access a particular Nastro instance."""
        return reverse('nastro-detail', args=[str(self.id)])   
    
    def __str__(self): 
        foglio = ''
        if self.tipologia == 'Servizio':
            foglio = ('%s/%s' % (self.linea, self.treno))
        elif self.tipologia == 'Riserva':
            foglio = ('%s %s %s' % (self.tipologia, self.ora_inizio.strftime("%H:%M"), self.polo_monta))
        else:
            foglio = ('%s %s' % (self.tipologia, self.ora_inizio.strftime("%H:%M")))        
        return '%s (%s | %s - %s %s)' % (foglio, self.ora_inizio.strftime("%H:%M"), self.ora_fine.strftime("%H:%M"), self.polo_monta, self.polo_smonta)

    def vista_semplice(self):   
        return '%s %s %s %s' % (self.ora_inizio.strftime("%H:%M"), self.ora_fine.strftime("%H:%M"), self.polo_monta, self.polo_smonta)

class StatoTurno(models.Model):
    stato = models.CharField(max_length=30, unique=True, null=False)    
    descrizione = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name_plural="Stati turno"
        ordering=['stato']
    
    def __str__(self):
        return self.stato
   
class Vettura(models.Model):
    numero = models.CharField(primary_key=True, unique=True, db_index=True, max_length=4, default='9999')
    descrizione = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural="Vetture"

    def __str__(self):
        return self.numero

class TurnoEffettivo(models.Model):
    data = models.DateField(editable=True, default=date.today,)
    operatore = models.ForeignKey(Operatore, on_delete=models.SET_NULL, null=True, related_name='operatore_di')

    linea = models.ForeignKey(Linea, to_field='nome', on_delete=models.SET_NULL, null=True)
    treno = models.CharField(max_length=4, blank=True, null=True)
    ora_inizio = models.TimeField(blank=True, null=True)
    ora_fine = models.TimeField(blank=True, null=True)
    polo_monta = models.CharField( 
        max_length=2,
        blank=True, 
        null=True,
        choices=POLO_OPZ,)
    polo_smonta = models.CharField( 
        max_length=2,
        blank=True, 
        null=True,
        choices=POLO_OPZ,)
    vetture = models.ManyToManyField('Vettura', through='VetturaPerTurno', through_fields=('turno','vettura'))

    creatore = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creatore_di')
    ultima_modifica = models.DateTimeField(auto_now=True, )
    stato = models.ForeignKey(StatoTurno, on_delete=models.SET_NULL, blank=True, null=True)
    """
    STATO_OPZ = (
        ('ci', 'check-in'),
        ('in', 'in corso...'),
        ('te', 'terminato'),
        ('an', 'annullato'),
        ('as', 'assente'),
        ('ca', 'cambio'),)
    stato = models.CharField( 
        max_length=2,
        blank=True, 
        null=True,
        choices=STATO_OPZ,)
    """

    #statiPresenzeGiornate

    note = models.TextField(max_length=500, blank=True, null=True)

    seguente = models.OneToOneField('self', models.SET_NULL, blank=True, null=True, related_name='seguente_di')# ,limit_choices_to = Q(precedente = None))
    precedente = models.OneToOneField('self', models.SET_NULL, blank=True, null=True, related_name='precedente_di') #,limit_choices_to=Q(seguente = None))
    
    class Meta:
        verbose_name_plural="Turni effettivi"
        ordering = ['data']
    
    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could
        # be replaced with super()).
        if len(values) != len(cls._meta.concrete_fields):
            values = list(values)
            values.reverse()
            values = [
                values.pop() if f.attname in field_names else DEFERRED
                for f in cls._meta.concrete_fields
            ]
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    """
    def save(self, aggiornaParenti = True, *args, **kwargs):    #aggiorna precedente o seguente 
        #do_something()
        #super().save(*args, **kwargs)  # Call the "real" save() method.
        #do_something_else()

        #LOGGING CALL *********************
        #logger.debug('Save - AggiornaParenti >> %s' % (aggiornaParenti))
        for i in args:
            logger.debug('Save - args >> %s' % i)
        for i in kwargs:
            logger.debug('Save - args >> %s' % i)
        #logger.debug('Save - self ------------ [[[ %s ]]] ------------' % self)
        #logger.debug('Save - self >> p: %s | s: %s' % (self.precedente, self.seguente))
        if self.seguente is not None: 
            s = self.seguente.precedente
            #logger.debug('Save - il precedente di %s è %s ' % ( self.seguente, s ))
        if self.precedente is not None: 
            p = self.precedente.seguente
            #logger.debug('Save - il seguente di %s è %s' % ( self.precedente, p))         
        
        #LOGICA 
        # TODO: aggiornare collegamenti
        
        if not self._state.adding and aggiornaParenti: # se il record non è nuovo recupera i vecchio valori
            vp = vs = None
            #logger.debug('Save - Record in aggiornamento. Carico vecchi collegamenti.')
            vp = self._loaded_values['precedente_id']
            vs = self._loaded_values['seguente_id']
            #logger.debug('Save - self _loaded_values >> %s' % self._loaded_values)
            #logger.debug('Save - self _loaded_values >> vs: %s | vp: %s' % ( vs, vp))
            if self.precedente_id != vp and vp is not None:
                #logger.debug('Save - precedente_id  >> Cambiato' )
                #vp->s = None save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vp)
                #logger.debug('Save - obj.s >> %s' % obj.seguente )
                obj.seguente = None
                obj.save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vp) 
                #logger.debug('Save - obj.s >> %s' % obj.seguente )             
            if self.seguente_id != vs and vs is not None:
                #logger.debug('Save - seguente_id  >> Cambiato' )
                #vs->p = None save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vs)
                #logger.debug('Save - obj.p >> %s' % obj.precedente )
                obj.precedente = None
                obj.save(aggiornaParenti = False)
                obj = Nastro.objects.get(pk=vs) # solo per debug
                #logger.debug('Save - obj.p >> %s' % obj.precedente )
                
        if self.precedente is not None and aggiornaParenti:
            #logger.debug('Save - precedente is not None' )
            self.precedente.seguente = self
            self.precedente.save(aggiornaParenti = False)
        if self.seguente is not None and aggiornaParenti:
            #logger.debug('Save - seguente is not None' )
            self.seguente.precedente = self
            self.seguente.save(aggiornaParenti = False)
        
        #super(Nastro, self).save(*args, **kwargs)
        super().save(*args, **kwargs)  # Call the "real" save() method.

    """
   
    """
    def get_absolute_url(self):        
        logger.debug('absolute!')
        #Returns the url to access a particular Nastro instance.
        return reverse('nastro-detail', args=[str(self.id)])
    """

    def __str__(self):
        return '%s/%s : %s %s - %s %s' % (self.linea.nome, self.treno, self.ora_inizio.strftime("%H:%M"), self.polo_monta, self.ora_fine.strftime("%H:%M"), self.polo_smonta)
    
    def vista_semplice(self):   
        return '%s %s %s %s' % (self.ora_inizio.strftime("%H:%M"), self.ora_fine.strftime("%H:%M"), self.polo_monta, self.polo_smonta)

class VetturaPerTurno(models.Model):
    vettura = models.ForeignKey(Vettura, on_delete=models.DO_NOTHING, null=False)
    turno = models.ForeignKey(TurnoEffettivo, on_delete=models.DO_NOTHING)
    data_e_ora_inizio_utilizzo = models.DateTimeField(null=True, blank=True)
    data_e_ora_fine_utilizzo = models.DateTimeField(null=True, blank=True)    

    note = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name_plural="Vetture dei turni effettivi"

    def __str__(self):
        return self.numero

class TurnoProgrammato(models.Model):
    data = models.DateField(editable=True, default=date.today,)
    operatore = models.ForeignKey(Operatore, on_delete=models.SET_NULL, null=True)
    nastro = models.ForeignKey(Nastro, on_delete=models.SET_NULL, null=True, )#limit_choices_to=Q(precedente = None))
    stato = models.ForeignKey(StatoTurno, on_delete=models.SET_NULL, blank=True, null=True)
    sostituto = models.ForeignKey(Operatore, on_delete=models.SET_NULL, blank=True, null=True, related_name="sostituto_di")
    vettura = models.ForeignKey(Vettura, on_delete=models.SET_NULL, blank=True, null=True)
    note = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural="Turni programmati"
        ordering = ['data', 'operatore']
        constraints = [
            models.UniqueConstraint(fields=['data', 'operatore', 'nastro'], name='unique_turno')
        ]  

    def nastro_completo(self):
        nastro = self.nastro
        if nastro is None: return ""
        #str_nastro = nastro.__str__()
        str_nastro = nastro.formated_foglio()
        #logger.debug('Turno >> nastro: %s str: %s s: %s' % (nastro, str_nastro, nastro.seguente))
        while (nastro.seguente is not None):
            nastro = nastro.seguente
            #str_nastro = str_nastro + " + " + nastro.__str__()
            str_nastro = str_nastro + nastro.formated_foglio()
        nastro = self.nastro
        while (nastro.precedente is not None):
            nastro = nastro.precedente
            #str_nastro = str_nastro + " + " + nastro.__str__()
            str_nastro = nastro.formated_foglio() + str_nastro
        return str_nastro

    #def get_absolute_url(self):
    #    return reverse('turnoprogrammato-detail', kwargs={'pk': self.pk})
    #def __str__(self):          
    #    return ('%s %s %s' % (defaultfilters.date(self.data,'D d/m/Y'), self.operatore, self.nastro_completo))


