SET SQL_SAFE_UPDATES = 0;
use ageco_new;

#Estrae il nominativo se non esiste
INSERT IGNORE INTO ageco_db_manager_operatore (ageco_db_manager_operatore.identificativo)
SELECT REPLACE(estratti.﻿Nominativo, '"', '') FROM estratti;

#Estrae la linea se non esiste
INSERT IGNORE INTO ageco_db_manager_linea (	
    ageco_db_manager_linea.nome,
    ageco_db_manager_linea.polo)
	#Seleziona tutte le linee con un polo
	SELECT Linea, Polo FROM
		(
			(
				SELECT DISTINCT t.Linea, IF(t.Monta = 'R8', t.Smonta , t.Monta) as Polo
				FROM estratti AS t			
			)
			UNION
			(
				SELECT DISTINCT t.Linea2, IF(t.Monta2 = 'R8', t.Smonta2 , t.Monta2) as Polo
				FROM estratti AS t
			)
			UNION
			(
				SELECT DISTINCT t.Linea3, IF(t.Monta3 = 'R8', t.Smonta3 , t.Monta3) as Polo
				FROM estratti AS t
			)		
		)AS origincon
	WHERE Polo != 'R8' or (Polo = 'R8' and Linea not in (
    #Seleziona tutte le linee con un polo che non sia R8
		SELECT Linea FROM
		(
			(
				SELECT DISTINCT t.Linea, IF(t.Monta = 'R8', t.Smonta , t.Monta) as Polo
				FROM estratti AS t
				Having Polo != 'R8'
			)
			UNION
			(
				SELECT DISTINCT t.Linea2, IF(t.Monta2 = 'R8', t.Smonta2 , t.Monta2) as Polo
				FROM estratti AS t
				Having Polo != 'R8'
			)
			UNION
			(
				SELECT DISTINCT t.Linea3, IF(t.Monta3 = 'R8', t.Smonta3 , t.Monta3) as Polo
				FROM estratti AS t
				Having Polo != 'R8'
			)		
		) as originsenza        
    )	)
	ORDER BY Linea;



#Estrae i nuovi nastri nella tabella nastro
INSERT IGNORE INTO ageco_db_manager_nastro (
	ageco_db_manager_nastro.tipologia,
	ageco_db_manager_nastro.fascia,
    ageco_db_manager_nastro.linea_id,
    ageco_db_manager_nastro.treno,
    ageco_db_manager_nastro.ora_inizio,
    ageco_db_manager_nastro.ora_fine,
    ageco_db_manager_nastro.polo_monta,
    ageco_db_manager_nastro.polo_smonta,
    ageco_db_manager_nastro.periodo_di_validita)
(SELECT DISTINCT
    t1.Tipologia,
    t1.Orario,
    t1.Linea,
    t1.Treno,
    STR_TO_DATE(t1.Inizio, '%H.%i') AS Inizio,
    STR_TO_DATE(t1.Fine, '%H.%i') AS Fine,
    t1.Monta,
    t1.Smonta,
    t1.Periodo
FROM
    estratti AS t1
WHERE t1.Inizio != '0.00')
UNION
(SELECT DISTINCT
    t2.Tipologia,
    t2.Orario,	
    t2.Linea2,
    t2.Treno2,
    STR_TO_DATE(t2.Inizio2, '%H.%i') AS Inizio,
    STR_TO_DATE(t2.Fine2, '%H.%i') AS Fine,
    t2.Monta2,
    t2.Smonta2,
    t2.Periodo
FROM
    estratti AS t2
WHERE t2.Inizio2 != '0.00')
UNION
(SELECT DISTINCT
    t3.Tipologia,
    t3.Orario,
    t3.Linea3,
    t3.Treno3,
    STR_TO_DATE(t3.Inizio3, '%H.%i') AS Inizio,
    STR_TO_DATE(t3.Fine3, '%H.%i') AS Fine,
    t3.Monta3,
    t3.Smonta3,
    t3.Periodo
FROM
    estratti AS t3
WHERE t3.Inizio3 != '0.00')
ORDER BY Tipologia , Linea , Inizio, Monta , Orario;


#Aggiunge se non esistono le colonne t t2, t3 alla tabella estratti
#e le aggiorna con gli id della tabella nastri???
DROP PROCEDURE IF EXISTS `aggiungi_colonne_turni`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `aggiungi_colonne_turni`(IN dbname VARCHAR(20))
BEGIN
IF NOT EXISTS( SELECT NULL
            FROM INFORMATION_SCHEMA.COLUMNS
           WHERE table_name = 'estratti'
             AND table_schema = dbname
             AND column_name = 't1')  THEN

  ALTER TABLE estratti ADD t1 INT(11) NULL;
END IF;
IF NOT EXISTS( SELECT NULL
            FROM INFORMATION_SCHEMA.COLUMNS
           WHERE table_name = 'estratti'
             AND table_schema = dbname
             AND column_name = 't2')  THEN

  ALTER TABLE estratti ADD t2 INT(11)  NULL;
END IF;
IF NOT EXISTS( SELECT NULL
            FROM INFORMATION_SCHEMA.COLUMNS
           WHERE table_name = 'estratti'
             AND table_schema = dbname
             AND column_name = 't3')  THEN

  ALTER TABLE estratti ADD t3 INT(11)  NULL;
END IF;
END$$
DELIMITER ;

CALL aggiungi_colonne_turni(DATABASE());

#Aggiorna i legami tra i turni nella tabella ageco_db_manager_nastro
UPDATE estratti AS e,
    ageco_db_manager_nastro AS t
SET
    e.t1 = t.id
WHERE
    t.Tipologia = e.Tipologia
        AND t.linea_id = e.Linea
        AND t.ora_inizio = STR_TO_DATE(e.Inizio, '%H.%i')
        AND t.ora_fine = STR_TO_DATE(e.Fine, '%H.%i')
        AND t.polo_monta = e.Monta
        AND t.periodo_di_validita = e.Periodo;

UPDATE estratti AS e,
    ageco_db_manager_nastro AS t
SET
    e.t2 = t.id
WHERE
    t.Tipologia = e.Tipologia
        AND t.linea_id = e.Linea2
        AND t.ora_inizio = STR_TO_DATE(e.Inizio2, '%H.%i')
        AND t.ora_fine = STR_TO_DATE(e.Fine2, '%H.%i')
        AND t.polo_monta = e.Monta2
        AND t.periodo_di_validita = e.Periodo;

UPDATE estratti AS e,
    ageco_db_manager_nastro AS t
SET
    e.t3 = t.id
WHERE
    t.Tipologia = e.Tipologia
        AND t.linea_id = e.Linea3
        AND t.ora_inizio = STR_TO_DATE(e.Inizio3, '%H.%i')
        AND t.ora_fine = STR_TO_DATE(e.Fine3, '%H.%i')
        AND t.polo_monta = e.Monta3
        AND t.periodo_di_validita = e.Periodo;

UPDATE estratti AS e,
    ageco_db_manager_nastro AS t
SET
    t.seguente_id = e.t2
WHERE
    t.Tipologia = e.Tipologia
        AND t.linea_id = e.Linea
        AND t.ora_inizio = STR_TO_DATE(e.Inizio, '%H.%i')
        AND t.ora_fine = STR_TO_DATE(e.Fine, '%H.%i')
        AND t.polo_monta = e.Monta
        AND t.periodo_di_validita = e.Periodo;

UPDATE estratti AS e,
    ageco_db_manager_nastro AS t
SET
    t.precedente_id = e.t1,
    t.seguente_id = e.t3
WHERE
    t.Tipologia = e.Tipologia
        AND t.linea_id = e.Linea2
        AND t.ora_inizio = STR_TO_DATE(e.Inizio2, '%H.%i')
        AND t.ora_fine = STR_TO_DATE(e.Fine2, '%H.%i')
        AND t.polo_monta = e.Monta2
        AND t.periodo_di_validita = e.Periodo;

UPDATE estratti AS e,
    ageco_db_manager_nastro AS t
SET
    t.precedente_id = e.t2
WHERE
    t.Tipologia = e.Tipologia
        AND t.linea_id = e.Linea3
        AND t.ora_inizio = STR_TO_DATE(e.Inizio3, '%H.%i')
        AND t.ora_fine = STR_TO_DATE(e.Fine3, '%H.%i')
        AND t.polo_monta = e.Monta3
        AND t.periodo_di_validita = e.Periodo;
        
#Popola tabella TurnoProgrammato
INSERT IGNORE INTO ageco_db_manager_turnoprogrammato(
	ageco_db_manager_turnoprogrammato.data,	
	ageco_db_manager_turnoprogrammato.nastro_id,	
    ageco_db_manager_turnoprogrammato.operatore_id
)
(SELECT DISTINCT    
	e.Data,
    e.t1,
	o.id    
FROM
	#estratti AS e JOIN dipendenti AS d ON e.﻿Nominativo = d.Identificativo)
	estratti AS e JOIN ageco_db_manager_operatore AS o ON REPLACE(e.﻿Nominativo, '"', '') = o.identificativo
WHERE e.t1 is not null
)
ORDER BY e.Data, o.id;       

INSERT IGNORE INTO ageco_db_manager_turnoprogrammato(
	ageco_db_manager_turnoprogrammato.data,	
	ageco_db_manager_turnoprogrammato.nastro_id,	
    ageco_db_manager_turnoprogrammato.operatore_id
)
(SELECT DISTINCT    
	e.Data,
    e.t2,
	o.id    
FROM
	#estratti AS e JOIN dipendenti AS d ON e.﻿Nominativo = d.Identificativo)
	estratti AS e JOIN ageco_db_manager_operatore AS o ON REPLACE(e.﻿Nominativo, '"', '') = o.identificativo
    WHERE e.t2 is not null
)
ORDER BY e.Data, o.id;

INSERT IGNORE INTO ageco_db_manager_turnoprogrammato(
	ageco_db_manager_turnoprogrammato.data,	
	ageco_db_manager_turnoprogrammato.nastro_id,	
    ageco_db_manager_turnoprogrammato.operatore_id
)
(SELECT DISTINCT    
	e.Data,
    e.t3,
	o.id    
FROM
	#estratti AS e JOIN dipendenti AS d ON e.﻿Nominativo = d.Identificativo)
	estratti AS e JOIN ageco_db_manager_operatore AS o ON REPLACE(e.﻿Nominativo, '"', '') = o.identificativo
    WHERE e.t3 is not null
)
ORDER BY e.Data, o.id;
        
SET SQL_SAFE_UPDATES = 1;