# !/bin/bash
if [ -z $1 ]; then
  echo Database non specificato!
  exit
else
  db=$1
fi
if [ -z $2 ]; then
  echo Database non specificato!
  exit
else
  psw=$2
fi
echo "*** Reset database iniziato... ***"
#bin/console cache:clear --env=prod
echo "*** Genero le entities ***"
#bin/console doctrine:generate:entities AppBundle --no-backup
echo "*** Elimino il vecchio database ***"
#bin/console doctrine:database:drop --force
echo "*** Creo il nuovo database ***"
#bin/console doctrine:database:create
echo "*** Aggiorno lo schema ***"
#bin/console doctrine:schema:update --force
echo "*** Importo i turni nella tabella estratti ***"
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200906.csv" -d2020/09/06 -v"Estivo 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200907.csv" -d2020/09/07 -v"Estivo 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200908.csv" -d2020/09/08 -v"Estivo 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200909.csv" -d2020/09/09 -v"Estivo 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200925.csv" -d2020/09/25 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200926.csv" -d2020/09/26 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200927.csv" -d2020/09/27 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20200928.csv" -d2020/09/28 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20201003.csv" -d2020/10/03 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20201004.csv" -d2020/10/04 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20201005.csv" -d2020/10/05 -v"Invernale 2020" --database=${db} --psw=${psw}
php ../Utili/importaturninew.php -f"../Utili/Turni/Turni 20201006.csv" -d2020/10/06 -v"Invernale 2020" --database=${db} --psw=${psw}

echo "*** Riempio le tabelle user, persona, tipoGiornta, sequenzeRiposi, situazioniParticolari***"
#mysql < "../Utili/dump5tabnew.sql"  --defaults-extra-file=../Utili/dbconfig.cnf --database=${db}
echo "*** Estraggo i turni dalla tabella estratti ***"
#mysql < "../Utili/estrai_nuovi_turni_new.sql"  --defaults-extra-file=../Utili/dbconfig.cnf --database=${db}
echo "*** Collego user <> dipendenti <> persona ***"
#mysql < "../Utili/collegaUserNew.sql"  --defaults-extra-file=../Utili/dbconfig.cnf --database=${db}
echo "*** Estraggo le linee ***"
#mysql < "../Utili/importalineenew.sql"  --defaults-extra-file=../Utili/dbconfig.cnf --database=${db}
echo "*** Fine reset ***"
