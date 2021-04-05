#ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password
#BY 'password';  

#SET GLOBAL local_infile=1;

SET FOREIGN_KEY_CHECKS = 0; 
TRUNCATE ageco_new.ageco_db_manager_nastro;
TRUNCATE ageco_new.ageco_db_manager_linea;
TRUNCATE ageco_new.ageco_db_manager_operatore;
TRUNCATE ageco_new.ageco_db_manager_turnoprogrammato;
TRUNCATE ageco_new.ageco_db_manager_turnoeffettivo;
TRUNCATE ageco_new.estratti;
SET FOREIGN_KEY_CHECKS = 1;


SET SQL_SAFE_UPDATES = 0;
UPDATE ageco_new.ageco_db_manager_turnoprogrammato AS t
SET t.data = '2020-11-25'
WHERE t.data = '2020-11-18';
UPDATE ageco_new.ageco_db_manager_turnoprogrammato AS t
SET t.data = '2020-11-26'
WHERE t.data = '2020-11-17';
UPDATE ageco_new.ageco_db_manager_turnoprogrammato AS t
SET t.data = '2020-11-27'
WHERE t.data = '2020-11-16';
UPDATE ageco_new.ageco_db_manager_turnoprogrammato AS t
SET t.data = '2020-11-28'
WHERE t.data = '2020-11-15';
SET SQL_SAFE_UPDATES = 1;

SET SQL_SAFE_UPDATES = 0;
UPDATE ageco_new.ageco_db_manager_turnoeffettivo AS t
SET t.data = '2020-11-25'
WHERE t.data = '2020-11-18';
SET SQL_SAFE_UPDATES = 1;