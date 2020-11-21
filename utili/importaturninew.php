<?php
$databasehost = "localhost"; // //"127.0.0.1";
$databaseport = 3308; //3306
$databasename = "ageco_new";
$databasetable = "estratti";
$databaseusername="root";
$databasepassword = "";
$fieldseparator = ";";
$lineseparator = "\n";
$csvfile_def = "Turni.csv";
$periodo = "Nessuno";
//$datecolumn = "'2017/1/11'";
$filesql = '../Utili/estrai_nuovi_turni_new.sql';
//var_dump($datacolumn);

$parametri = getopt("f::d::v::ip:",array("database::", "psw::"));
echo "\n";
print_r('es. php ../Utili/importa.php -f"../Utili/Turni/Turni 20170120.csv" -d2017/01/20 -v"Inverno 2016"');
//print_r($parametri);
//var_dump($parametri);
$interattivo = isset($parametri["i"]) ? true : false;
//var_dump($interattivo);
$databasename = isset($parametri["database"]) ? $parametri["database"] : $databasename;
//var_dump($databasename);
$databasepassword = isset($parametri["psw"]) ? $parametri["psw"] : $databasepassword;
//var_dump($databasepassword);
$periodo = "'".(isset($parametri["v"]) ? $parametri["v"] : $periodo)."'";
var_dump($periodo);

$csvfile = isset($parametri["f"]) ? $parametri["f"] : $csvfile_def;
print_r ("\nSto per caricare i dati del file '".$csvfile."' nella tabella ".$databasetable." del database.\n");
$datecolumn = "'".(isset($parametri["d"]) ? $parametri["d"] : date('Y-m-d'))."'";
print_r("Con la data ".$datecolumn.". \n");
if ($interattivo){
  echo "\nATTENZIONE! Controlla il nome del file e la data (formato YYYY/MM/DD).\n\nSei sicuro di voler continuare? [Si]";
  $handle = fopen ("php://stdin","r");
  $line = fgetc($handle);
  if(($line == 'n') OR ($line == 'N')){
      echo "\nCaricamento annullato!\n";
      exit;
  }
  fclose($handle);
}
echo "\n";
echo "Caricamento in corso...\n";

if(!file_exists($csvfile)) {
    die("\nFile not found. Make sure you specified the correct path.\n");
}
// Read in only first row of CSV file
$handle = fopen($csvfile, "r");

$row = 1;
$columns = [];
while (($data = fgetcsv($handle, 1000, ";")) !== FALSE AND $row==1) {
   $columns = $data;
   $row++;
}
//var_dump($columns);

$counters = array_count_values($columns);
//var_dump($counters);
$columns = array_reverse ($columns);
foreach ($columns as $key => $value){
  //var_dump($counters[$value]);
  if ($counters[$value]> 1){
    //var_dump($value);
    $columns[$key] = $value.$counters[$value]--;
    //var_dump($value);
  }
}
$columns = array_reverse ($columns);
//var_dump($columns);
//array_push($columns, "Periodo");
//var_dump($columns);

try {   //
    //$pdo = new PDO("mysql:host=$databasehost;port=$databaseport;dbname=$databasename",
    $pdo = new PDO("mysql:unix_socket=/tmp/mysql.sock;dbname=$databasename",
        $databaseusername, $databasepassword,
        array(
            PDO::MYSQL_ATTR_LOCAL_INFILE => true,
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        )
    );
    echo "Connected successfully\n";
} catch (PDOException $e) {
    die("database connection failed: ".$e->getMessage())."\n";
}
//var_dump($columns);
//SQL string commands
$str = "CREATE TABLE IF NOT EXISTS $databasetable (`"
              .implode("` VARCHAR(50) NOT NULL, `", $columns)
              ."` VARCHAR(50) NOT NULL,"
              ." id int UNSIGNED NOT NULL AUTO_INCREMENT,"
              ." Data DATE NOT NULL,"  //" DEFAULT ".$datecolumn.", "
              ." Periodo VARCHAR(100) NOT NULL,"
              ." PRIMARY KEY (id),"
              ." UNIQUE INDEX `estratti_UNIQUE` (`$columns[0]` ASC, `Data` ASC));";
echo "\n Crea tabella se non esiste.."/*."\n".$str."\n"*/;
$createSQL = $pdo->exec($str);
echo "\n Risposta creazione: $createSQL \n";

$str = "LOAD DATA LOCAL INFILE ".$pdo->quote($csvfile)." INTO TABLE `$databasetable`
      FIELDS TERMINATED BY ".$pdo->quote($fieldseparator)."
      LINES TERMINATED BY ".$pdo->quote($lineseparator)."
      IGNORE 1 LINES SET Data = ".$datecolumn.", Periodo = ".$periodo;
echo "\n Query SQL per il caricamento: \n   ".$str;
$affectedRows = $pdo->exec($str);
echo "\n Caricati un totale di $affectedRows records dal file csv.\n";

//system("mysql -u$databaseusername -p$databasepassword $databasename < $filesql");

?>
