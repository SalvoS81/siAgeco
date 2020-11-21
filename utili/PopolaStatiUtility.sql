use ageco_new;

SELECT distinctrow operatore_id FROM ageco_db_manager_turnoprogrammato
WHERE data = '2020-11-16';

SELECT * FROM ageco_db_manager_turnoprogrammato
WHERE data = '2020-11-16'
ORDER BY RAND()
LIMIT 5;

SELECT * FROM ageco_db_manager_turnoprogrammato
WHERE data = '2020-11-16' and operatore_id in 
	(
		SELECT distinctrow operatore_id FROM ageco_db_manager_turnoprogrammato
		WHERE data = '2020-11-16'
        ORDER BY RAND()
		LIMIT 5
	);

 
SELECT t.* FROM ageco_db_manager_turnoprogrammato as t
inner join 
(
	SELECT distinctrow operatore_id FROM ageco_db_manager_turnoprogrammato
	WHERE data = '2020-11-16'
	ORDER BY RAND()
	LIMIT 5 
) as x
where t.data = '2020-11-16' and t.operatore_id = x.operatore_id and t.stato_id is null;


set @x = (SELECT percentuale FROM percentuali_stato WHERE stato = 2);
SELECT @x;

SET @numero_stati = (SELECT MAX(stato) FROM percentuali_stato );
SELECT @numero_stati;


UPDATE ageco_db_manager_turnoprogrammato as t,
	(
		SELECT t.* FROM ageco_db_manager_turnoprogrammato as t
		inner join 
		(
			SELECT distinctrow operatore_id FROM ageco_db_manager_turnoprogrammato
			WHERE data = '2020-11-16'
			ORDER BY RAND()
			LIMIT 5 
		) as x
		where t.data = '2020-11-16' and t.operatore_id = x.operatore_id and t.stato_id is null
	) as f
SET t.stato_id = 1
where t.id = f.id;

SELECT * FROM ageco_db_manager_turnoprogrammato where stato_id is not null and data = '2020-11-18';

SELECT * FROM ageco_db_manager_turnoprogrammato where data = '2020-11-18';

UPDATE ageco_db_manager_turnoprogrammato as t,
(
	SELECT * FROM ageco_db_manager_turnoprogrammato where data = '2020-11-18'
) as f
SET t.stato_id = null
where t.id = f.id; 


SET @numero_turni = (SELECT count(*) FROM ageco_db_manager_turnoprogrammato WHERE data = '2020-11-18');
SELECT @numero_turni;


# imposta lo stato dei turni oltre una certa ora a null
UPDATE ageco_db_manager_turnoprogrammato as t,
(
	SELECT t.id FROM ageco_db_manager_turnoprogrammato as t
	INNER JOIN ageco_db_manager_nastro as n 
		on t.nastro_id = n.id
		and t.data = '2020-11-18'
		and n.ora_inizio > '12:00'
	order by n.ora_inizio
) as f
SET t.stato_id = null
where t.id = f.id;


# selezione per ora inizio
SELECT * FROM ageco_db_manager_turnoprogrammato as t
INNER JOIN ageco_db_manager_nastro as n 
	on t.nastro_id = n.id
    and t.data = '2020-11-18'
    and n.ora_inizio > '12:00'
order by n.ora_inizio;

# selezione stato non null
SELECT * FROM ageco_db_manager_turnoprogrammato as t
INNER JOIN ageco_db_manager_nastro as n 
	on t.nastro_id = n.id
    and t.data = '2020-11-18'
    and t.stato_id is not null
order by n.ora_inizio;	

#popola turno effettivo
SET FOREIGN_KEY_CHECKS = 0;
INSERT IGNORE INTO ageco_db_manager_turnoeffettivo
SELECT 
		0,
		t.data,
        n.treno,
        n.ora_inizio,
        n.ora_fine,
        n.polo_monta,
        n.polo_smonta,
        now(),
        t.stato_id,
        t.note,
        null,
        n.linea_id,
        t.operatore_id,
        n.precedente_id,
        n.seguente_id
FROM ageco_db_manager_turnoprogrammato as t
INNER JOIN ageco_db_manager_nastro as n 
	on t.nastro_id = n.id
	and t.data = '2020-11-18'
	and t.stato_id is not null
order by n.linea_id, n.treno;
SET FOREIGN_KEY_CHECKS = 1;


# selezione stato non null
SELECT 
		0,
		t.data,
        n.treno,
        n.ora_inizio,
        n.ora_fine,
        n.polo_monta,
        n.polo_smonta,
        now(),
        t.stato_id,
        t.note,
        null,
        n.linea_id,
        t.operatore_id,
        n.precedente_id,
        n.seguente_id
FROM ageco_db_manager_turnoprogrammato as t
INNER JOIN ageco_db_manager_nastro as n 
	on t.nastro_id = n.id
	and t.data = '2020-11-18'
	and t.stato_id is not null
order by n.linea_id, n.treno
#limit 136;



