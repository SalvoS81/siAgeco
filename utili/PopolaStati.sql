DROP PROCEDURE PopolaStati;

DELIMITER $$
CREATE PROCEDURE PopolaStati()
BEGIN
	DECLARE numero_stati  INT;
    DECLARE data_scelta DATE;
    DECLARE numero_turni int;
    DECLARE x INT;
    DECLARE p INT;
    DECLARE turni_percentuale INT;
    DECLARE turni_somma INT DEFAULT 0;
    
	SET data_scelta = '2020-11-18';
    
    SET x = 1;
    SET p = 0;
	SET numero_stati = (SELECT MAX(stato) FROM ageco_new.percentuali_stato );
    SET numero_turni = (SELECT count(*) 
						FROM 
							(
								SELECT distinctrow operatore_id FROM ageco_new.ageco_db_manager_turnoprogrammato
								WHERE data = data_scelta and stato_id is null
							) as t
						);
    SELECT numero_stati, numero_turni;
	
    WHILE x < numero_stati + 1 DO
		set p = (SELECT percentuale FROM ageco_new.percentuali_stato WHERE stato = x);
		set turni_percentuale = (numero_turni * p) / 100;
        SET turni_somma = turni_somma + turni_percentuale;
        SELECT x, p, turni_percentuale, turni_somma;

        UPDATE ageco_new.ageco_db_manager_turnoprogrammato as t,
		(
			SELECT t.* FROM ageco_new.ageco_db_manager_turnoprogrammato as t
			inner join 
			(
				SELECT distinctrow operatore_id FROM ageco_new.ageco_db_manager_turnoprogrammato
				WHERE data = data_scelta and stato_id is null
				ORDER BY RAND()
				LIMIT turni_percentuale 
			) as x
			where t.data = data_scelta and t.operatore_id = x.operatore_id
		) as f
		SET t.stato_id = x
		where t.id = f.id;
        
        SET x = x + 1;
	END WHILE;
END$$

DELIMITER ;

CALL PopolaStati;