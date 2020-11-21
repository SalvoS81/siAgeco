================================
Documento di Analisi e Specifica
================================


Indice
______


`1 Introduzione`_

  `1.1 Scopo del documento`_

  `1.2 Descrizione del documento`_

  `1.3 Target e funzionalità dell’applicazione`_

`2 Glossario`_

`3 Modelli del sistema`_

  `3.1 Utilizzi per l'attore Graduato`_

  `3.1.1 Accesso al sistema`_

  `3.1.2 Foglio uscita servizio`_

  `3.1.3 Presenza o assenza`_

`4 Definizione dei requisiti funzionali`_

`5 Definizione dei requisiti non funzionali`_

  `5.1 Requisiti di prodotto`_

  `5.2 Requisiti di processo`_

  `5.3 Requisiti esterni`_

`6 Evoluzione del sistema`_

`7 Specifiche dei requisiti`_

`8 Appendice`_

  `8.1 Requisiti del dispositivo`_



----



1 Introduzione
==============

1.1 Scopo del documento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*(bozza)*
Lo scopo del presente documento è quello di fornire informazioni dettagliate
per lo sviluppo e l’implementazione dell’applicazione "Ageco".
Il documento inoltre, rende note le diverse funzionalità che l’applicazione offrirà agli
utenti finali. Le decisioni, in materia di progettazione non sono contemplate
in questo documento.

1.2 Descrizione del documento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il documento è composto dalle seguenti sezioni:

  • **Glossario:** descrizione di termini tecnici e acronimi, usati all’interno del documento e normalmente non riconosciuti da un utente non esperto.

  • **Modelli di sistema:** analisi del sistema attraverso l’utilizzo del linguaggio UML. L’analisi viene fatta fornendo i diversi casi d’uso che descrivono i comportamenti di un ipotetico utente che si interfaccia con l’applicazione.

  • **Definizione dei requisiti funzionali:** descrizione dei servizi che il sistema fornisce all’utente finale.

  • **Definizione dei requisiti non funzionali:** descrizione dei vincoli che il sistema è chiamato a rispettare.

  • **Evoluzione del sistema:** Assunzioni su cui si basa il sistema e indicazione di eventuali cambiamenti o evoluzione delle funzionalità presenti nel sistema.

  • **Specifica dei requisiti:** Riepilogo dei requisiti funzionali

  • **Appendice:** Descrizione della piattaforma hardware e del database.

1.3 Target e funzionalità dell’applicazione
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*(bozza)*
Ageco è un prototipo di sistema informativo che consentirà di gestire
il personale in servizio di linea con modalità simili a quelle usate nei
prestampati cartacei utilizzati dagli addetti all'esercizio.
Il sistema permetterà inoltre di:

- Raccogliere dati sul esercizio in tempo reale.

- Produrre e visionare i report della posizione.

- Produrre l'elenco con i turni effettivi svolti dai conducenti.

----

2 Glossario
===========

+------------------------+------------------------------------------------------+-----------------------+
| Termine                | Definizione                                          |Sinonimo               |
+========================+======================================================+=======================+
| Coordinatore           | Lavoratori che, in possesso di adeguate competenze   | Parametro 210         |
|                        | tecniche e gestionali, svolgono, con margini di      |                       |
|                        | discrezionalità e di iniziativa, attività di         | Coordinatore          |
|                        | coordinamento degli operatori e degli addetti anche  | d'esercizio           |
|                        | mediante l'eventuale responsabilità di unità         |                       |
|                        | operative nei settori del movimento e traffico       |                       |
|                        | automobilistico e/o filotranviario. fonte: CCNL 2000 |                       |
|                        | Autoferrotranvieri                                   |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Graduato               | Lavoratori che, in possesso di adeguata competenza   | Parametro 193         |
|                        | comunque acquisita nei settori del movimento         |                       |
|                        | automobilistico e/o in quello filotranviario,        | Addetto all'esercizio |
|                        | svolgono attività di coordinamento degli operatori,  |                       |
|                        | di controllo sulla regolarità dell'esercizio, sul    |                       |
|                        | personale viaggiante, […].  fonte: CCNL 2000         |                       |
|                        | Autoferrotranvieri                                   |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Conducente             | Lavoratori che, in possesso delle abilitazioni       | Parametro 140, 158,   |
|                        | richieste, svolgono mansioni di guida di mezzi       | 175, 183              |
|                        | aziendali per il trasporto di persone […].           | Operatore d'esercizio |
|                        | fonte: CCNL 2000 Autoferrotranvieri                  |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Ripresa                | Come da CCNL è l’intervallo che intercorre tra ora   | Turno, Spezzone       |
|                        | inizio lavoro ed ora fine lavoro, in una unica       |                       |
|                        | linea.                                               |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Nastro di lavoro       | Come da CCNL è l’intervallo tra l’inizio             |                       |
|                        | della prima ripresa e la fine dell’ultima ripresa.   |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Nastro predefinito     | È definito nel documento come l’insieme delle        | Nastro                |
|                        | informazioni riguardanti una o più riprese con       |                       |
|                        | l’aggiunta dei rispettivi: luogo inizio lavoro,      |                       |
|                        | luogo fine lavoro, linea e treno.                    |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Turno programmato      | È definito nel documento come l’assegnazione         |                       |
|                        | d’ufficio di un nastro predefinito ad un             |                       |
|                        | determinato conducente in una determinata data.      |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Turno effettivo        | È il turno effettivamente lavorato dal conducente    |                       |
|                        | in una determinata data. Non necessariamente         |                       |
|                        | corrisponde a quello preassegnato. Serve a           |                       |
|                        | quantificare le ore di lavoro da retribuire, i       |                       |
|                        | valori di produzione e l’andamento del servizio.     |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Gestione del servizio  | È l’insieme delle attività che il Coordinatore e     |                       |
|                        | il Graduato svolgono per garantire la regolarità     |                       |
|                        | dell’esercizio.                                      |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Foglio uscita servizio | È un elenco in cui sono riportati i turni di servizio|                       |
|                        | in un determinato polo in una determinata data.      |                       |
|                        | Ordinati per ora di inizio lavoro.                   |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Report posizione       | È un insieme di documenti che riportano informazioni |                       |
|                        | rilevanti sullo stato del servizio.                  |                       |
|                        | Ad esempio, il numero di personale assente,          |                       |
|                        | il numero di vetture in linea o altro.               |                       |
+------------------------+------------------------------------------------------+-----------------------+
| Esercizio              | È l'attività svolta dall'azienda.                    |                       |
|                        | La fornitura del servizio di trasporto di linea.     |                       |
+------------------------+------------------------------------------------------+-----------------------+
| xxxx                   |                                                      |                       |
+------------------------+------------------------------------------------------+-----------------------+

----


3 Modelli del sistema
=====================

In questa sezione verranno elencati i casi d’uso del sistema, ossia i possibili
modi di utilizzo del sistema, per farlo cominceremo con l'individuare i possibili
attori (vedi Tabella 3a).


  +-----------------+---------------------------------------------------+
  | Attore          | Obiettivi primari relativi al sistema             |
  +=================+===================================================+
  | Graduato        | Gestire il servizio                               |
  +-----------------+---------------------------------------------------+
  | Coordinatore    | Analizzare i report della posizione               |
  +-----------------+---------------------------------------------------+
  | Ufficio paghe   | Raccogliere i dati sulle presenze del personale   |
  +-----------------+---------------------------------------------------+

  *Tabella 3a: Elenco degli Attori.*

|

Successivamente attraverso un diagramma UML daremo una prima rappresentazione
più astratta (vedi Figura 3a) nella quale mostreremo i diversi scenari in cui
i diversi attori interagiscono con il sistema.

  .. figure:: media/casiduso/generale.png
     :align: center
     :scale: 100%

     *Figura 3a: Casi d'uso - astrazione generale - livello summary.*

|

Note: L'attore coordinatore ha accesso anche ai casi d'uso del graduato.

*(bozza)*
Ed in fine passeremo all'analisi in dettaglio dei casi d'uso più significativi,
tralasciando quelli ripetitivi. L'analisi dei singoli casi si compone di una breve
descrizione come in (Tabella 3b) e di diagrammi UML per singolo attore.

  +-----------------+------------------------------------------------------------------+
  | Nome caso d'uso | Nome                                                             |
  +-----------------+------------------------------------------------------------------+
  | Obiettivo       | Descrizione della funzionalità fornita dal sistema, che va       |
  |                 | incontro ad una necessità dell’utente                            |
  +-----------------+------------------------------------------------------------------+
  | Attori          | Persone, dispositivi o altre entità che interagiscono con il     |
  |                 | sistema                                                          |
  +-----------------+------------------------------------------------------------------+
  | Pre-condizioni  | Condizioni che devono esistere all’inizio del caso d’uso e che   |
  |                 | attivano il suo verificarsi                                      |
  +-----------------+------------------------------------------------------------------+
  | Trigger         | Evento che attiva il caso d’uso                                  |
  +-----------------+------------------------------------------------------------------+
  | Descrizione     | Descrizione della sequenza di interazione fra attori e sistema   |
  +-----------------+------------------------------------------------------------------+
  | Alternative     | Descrizione delle variazioni di sequenze percorribili            |
  |                 | dagli attori.                                                    |
  +-----------------+------------------------------------------------------------------+
  | Post-condizioni | Condizioni che devono esistere al termine del caso d’uso.        |
  +-----------------+------------------------------------------------------------------+

  *Tabella 3b: Template di base per la descrizione dei casi d’uso*


3.1 Utilizzi per l'attore Graduato
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|

  .. figure:: media/casiduso/graduato.png
     :align: center
     :scale: 100%

     *Figura 3.1a: Casi d'uso - Diagramma UML per l'attore graduato - livello user-goal*

|

3.1.1 Accesso al sistema
~~~~~~~~~~~~~~~~~~~~~~~~~

  +-----------------+------------------------------------------------------------------+
  | Nome caso d'uso | Accesso al sistema                                               |
  +-----------------+------------------------------------------------------------------+
  | Obiettivo       | Accedere alle funzioni del sistema                               |
  +-----------------+------------------------------------------------------------------+
  | Attori          | Graduato                                                         |
  +-----------------+------------------------------------------------------------------+
  | Pre-condizioni  | Aver avviato il browser del dispositivo /                        |
  |                 | Il Graduato possiede matricola e pin per accedere al sistema.    |
  +-----------------+------------------------------------------------------------------+
  | Trigger         | Aver visualizzato la pagina di login                             |
  +-----------------+------------------------------------------------------------------+
  | Descrizione     |  1. Digitare e confermare l'indirizzo web del sistema nella      |
  |                 |     barra dell'indirizzo nel browser.                            |
  |                 |                                                                  |
  |                 |  2. Visualizzare la pagina di login.                             |
  |                 |                                                                  |
  |                 |  3. Digitare matricola e pin.                                    |
  |                 |                                                                  |
  |                 |  4. Cliccare su accedi.                                          |
  |                 |                                                                  |
  |                 |  5. Visualizzare la schermata principale del sistema.            |
  +-----------------+------------------------------------------------------------------+
  | Alternative     |  5a.  Comunicare che matricola e pin non sono riconosciuti.      |
  |                 |                                                                  |
  |                 |  5b.  Riproporre la pagina di login.                             |
  +-----------------+------------------------------------------------------------------+
  | Post-condizioni | Il Graduato visualizza la schermata principale del sistema.      |
  +-----------------+------------------------------------------------------------------+

  *Tabella 3.1.1: Caso d'uso C0*

3.1.2 Foglio uscita servizio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  +-----------------+------------------------------------------------------------------+
  | Nome caso d'uso | Consultazione foglio uscita servizio.                            |
  +-----------------+------------------------------------------------------------------+
  | Obiettivo       | Visualizzare l'elenco dei turni relativi alla data odierna.      |
  +-----------------+------------------------------------------------------------------+
  | Attori          | Graduato                                                         |
  +-----------------+------------------------------------------------------------------+
  | Pre-condizioni  | Aver avuto accesso al sistema.                                   |
  +-----------------+------------------------------------------------------------------+
  | Trigger         | Aver cliccato la voce "Foglio servizio" nel menu principale.     |
  +-----------------+------------------------------------------------------------------+
  | Descrizione     |  1. Click su "Foglio servizio" nel menu.                         |
  |                 |                                                                  |
  |                 |  2. Visualizzazione del foglio uscita servizio.                  |
  |                 |                                                                  |
  |                 |  3. Interazioni da parte del Graduato.                           |
  +-----------------+------------------------------------------------------------------+
  | Alternative     |  N/D                                                             |
  +-----------------+------------------------------------------------------------------+
  | Post-condizioni | Il Graduato visualizza il foglio uscita servizio.                |
  +-----------------+------------------------------------------------------------------+

  *Tabella 3.1.2: Caso d'uso C1*

3.1.3 Presenza o assenza
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  +-----------------+------------------------------------------------------------------+
  | Nome caso d'uso | Registrazione stato conducente.                                  |
  +-----------------+------------------------------------------------------------------+
  | Obiettivo       | Registrare la presenza/assenza di un conducente.                 |
  +-----------------+------------------------------------------------------------------+
  | Attori          | Graduato                                                         |
  +-----------------+------------------------------------------------------------------+
  | Pre-condizioni  | Aver individuato il turno nel foglio uscita servizio.            |
  +-----------------+------------------------------------------------------------------+
  | Trigger         | Aver cliccato sul tasto "registra" nella riga del turno.         |
  +-----------------+------------------------------------------------------------------+
  | Descrizione     |  1. Click su "registra" nella riga del turno.                    |
  |                 |                                                                  |
  |                 |  2. Apertura schermata con elenco di scelte possibili.           |
  |                 |                                                                  |
  |                 |  3. Selezione della stato del conducente.                        |
  |                 |                                                                  |
  |                 |  4. Click su "salva".                                            |
  |                 |                                                                  |
  |                 |  5. Visualizzare foglio uscita servizio aggiornato.              |
  +-----------------+------------------------------------------------------------------+
  | Alternative     |  3a. Click sul tasto "annulla".                                  |
  +-----------------+------------------------------------------------------------------+
  | Post-condizioni | - Il Graduato visualizza il foglio uscita servizio.              |
  |                 | - Lo stato del conducente è aggiornato.                          |
  +-----------------+------------------------------------------------------------------+

  *Tabella 3.1.3: Caso d'uso C2*


*(continua...) (in attesa)*


----

4 Definizione dei requisiti funzionali
======================================
In questa sezione verranno esposti i principali requisiti funzionali
dell’applicazione Ageco, ossia le funzionalità e i servizi che il sistema fornisce all'utente finale.
Lo schema utilizzato per la descrizione dei requisiti funzionali è il seguente:

  +----------------+------------------------------------------------------------------+
  | Nome           | Nome del requisito funzionale                                    |
  +----------------+------------------------------------------------------------------+
  | ID             | Identificativo del requisito                                     |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Descrizione della specifica funzione                             |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Motivo per cui è necessario il requisito                         |
  +----------------+------------------------------------------------------------------+
  | Influisce      | Come interagisce con altre funzionalità                          |
  +----------------+------------------------------------------------------------------+
  | Specifica      | Codice della relativa specifica                                  |
  +----------------+------------------------------------------------------------------+
  | Attore         | Attore che richiede la funzione                                  |
  +----------------+------------------------------------------------------------------+

  Tabella 4: Template per la descrizione dei requisiti funzionali

|

  +----------------+------------------------------------------------------------------+
  | Nome           | Accesso autenticato al sistema                                   |
  +----------------+------------------------------------------------------------------+
  | ID             | RF01                                                             |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Collegandosi al sistema attraverso un browser internet           |
  |                | viene mostrata una pagina di login per autenticare l'utente.     |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Consentire l'accesso alle funzioni del sistema solo a utenti     |
  |                | riconosciuti.                                                    |
  +----------------+------------------------------------------------------------------+
  | Influisce      | E' il passaggio obbligato per accedere alle funzioni del sistema.|
  +----------------+------------------------------------------------------------------+
  | Specifica      | S01                                                              |
  +----------------+------------------------------------------------------------------+
  | Attore         | Tutti                                                            |
  +----------------+------------------------------------------------------------------+

  Tabella 4a: RF01 - Accesso autenticato al sistema

|

  +----------------+------------------------------------------------------------------+
  | Nome           | Schermata principale                                             |
  +----------------+------------------------------------------------------------------+
  | ID             | RF02                                                             |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | E' la pagina che viene mostrata quando si ha accesso al sistema, |
  |                | mostra pulsanti e menu che permettono di passare alle funzioni   |
  |                | del sistema.                                                     |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Mostrare tutte le funzioni del sistema.                          |
  +----------------+------------------------------------------------------------------+
  | Influisce      | E' il punto di partenza di tutte le funzioni del sistema.        |
  +----------------+------------------------------------------------------------------+
  | Specifica      | S02                                                              |
  +----------------+------------------------------------------------------------------+
  | Attore         | Tutti                                                            |
  +----------------+------------------------------------------------------------------+

  Tabella 4b: RF02 - Schermata principale

|

*(continua...) (in attesa)*

----

5 Definizione dei requisiti non funzionali
==========================================

In questa sezione verranno esposti i principali requisiti non funzionali
dell’applicazione Ageco, ovvero la descrizione dei vincoli e delle proprietà
che il sistema è tenuto a rispettare.
Lo schema utilizzato per la descrizione dei requisiti non funzionali è il seguente:

  +----------------+------------------------------------------------------------------+
  | ID             | Identificativo del requisito                                     |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Descrizione del requisito non funzionale                         |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Motivo per cui è necessario il requisito                         |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Tipologia di requisito non funzionale                            |
  +----------------+------------------------------------------------------------------+

  Tabella 5: Template per la descrizione dei requisiti non funzionali

|

5.1 Requisiti di prodotto
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Descrizione delle proprietà e delle caratteristiche che il prodotto deve possedere.

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF01                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Il sistema deve essere fluido e avere tempi di risposta          |
  |                | inferiori a tre secondi.                                         |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | La lentezza potrebbe rallentare e compromettere il lavoro degli  |
  |                | operatori e quindi la fruizione del servizio da parte degli      |
  |                | utenti aziendali.                                                |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Perfomance                                                       |
  +----------------+------------------------------------------------------------------+

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF02                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Il sistema deve avere un aspetto familiare per gli utenti e      |
  |                | utilizzare testi e colori già conosciuti.                        |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Il passaggio dal sistema tradizionale a quello informatizzato    |
  |                | deve essere il più rapido possibile anche per gli utenti         |
  |                | meno esperti.                                                    |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Usabilità                                                        |
  +----------------+------------------------------------------------------------------+

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF03                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Il sistema deve essere stabile e prevedere un sistema per        |
  |                | il recupero immediato delle funzionalità in caso di crash.       |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Le funzioni del sistema sono vitali per l'andamento              |
  |                | dell'esercizio aziendale.                                        |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Affidabilità                                                     |
  +----------------+------------------------------------------------------------------+

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF04                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Il sistema deve essere accessibile dal maggior numero di         |
  |                | dispositivi possibili in grado di navigare in internet.          |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Facilità di trovare dispositivi hardware idonei,                 |
  |                | sicurezza in caso di crash hardware.                             |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Portabilità                                                      |
  +----------------+------------------------------------------------------------------+

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF05                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Il sistema deve essere in grado di assorbire facilmente          |
  |                | cambiamenti dei requisiti.                                       |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | L'aggiunta di funzionalità deve essere veloce e potenzialmente   |
  |                | illimitatà.                                                      |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Estendibilità                                                    |
  +----------------+------------------------------------------------------------------+

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF06                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Consiste nella facilità di installare, controllare il sistema ed |
  |                | intervenire per renderlo nuovamente operativo qualora si         |
  |                | verifichi un'interruzione del funzionamento.                     |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Il sistema deve essere ripristinato velocemente per evitare      |
  |                | interruzioni dell'esercizio aziendale.                           |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Manutenibilità                                                   |
  +----------------+------------------------------------------------------------------+

|

  +----------------+------------------------------------------------------------------+
  | ID             | RNF07                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Disponibilità di un buon livello di documentazione del sistema,  |
  |                | realizzata con strumenti standard.                               |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | E' indispensabile per una buona presentazione del prodotto       |
  |                | software al committente e agevola un eventuale refactoring       |
  |                | dell'applicazione.                                               |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Adeguata Documentazione                                          |
  +----------------+------------------------------------------------------------------+

|

5.2 Requisiti di processo
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Descrizione delle scelte e le procedure organizzative che influiscono sul sistema.

  +----------------+------------------------------------------------------------------+
  | ID             | RNF08                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Il sistema deve essere sviluppato con linguaggi di               |
  |                | programmazione altamente diffusi.                                |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Permettere l'aggiornamento e la manutenzione da parte di un      |
  |                | alto numero di sviluppatori.                                     |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Implementazione                                                  |
  +----------------+------------------------------------------------------------------+

|


5.3 Requisiti esterni
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descrizione dei fattori esterni al sistema che influiscono sul sistema.

  +----------------+------------------------------------------------------------------+
  | ID             | RNF09                                                            |
  +----------------+------------------------------------------------------------------+
  | Descrizione    | Capacità del sistema di interagire con altri sistemi esterni.    |
  +----------------+------------------------------------------------------------------+
  | Motivazione    | Il sistema deve essere scambiare dati con gli altri sistemi      |
  |                | informativi aziendali.                                           |
  +----------------+------------------------------------------------------------------+
  | Tipo           | Interoperabilità                                                 |
  +----------------+------------------------------------------------------------------+

|


6 Evoluzione del sistema
======================================

...

7 Specifiche dei requisiti
======================================

...

8 Appendice
======================================

...

8.1 Requisiti del dispositivo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

...
