

var url_intranet = 'http://intranet.amt.ct.it/tests/auth.php?';

//Debug Area
function myGetJSON(url, callback) {
    //console.log(url);
    var x;
    var urlTipo = ['/auth.php?', '/leggi_giorni.php?', '/leggi_turno.php?'];
    for (x = 0; x < urlTipo.length; x++) {
        if (url.search(urlTipo[x]) > 0)
            break;
    }
    switch (x) {
        case 0:
            {
              var user = url.match("user=(.*)&");
              //messaggio("<b>debug:</b> "+"myGetJSON user: "+user[1]);
              switch (user[1]) {
                case "64945":
                  x = {"logged": true, "versione": "2.0", "distintivo": "SICALI 5", "nome": "SICALI SALVATORE", "sessione": "a5158e504228f90e28dea90693cccee1"};
                  break;
                case "33123":
                  x = {"logged": true, "versione": "2.0", "distintivo": "CICCIO 5", "nome": "CICCIO SALVATORE", "sessione": "a5158e504228f90e28dea90693cccee1"};
                  break;
                case "22123":
                  x = {"logged": true, "versione": "2.0", "distintivo": "CAIO 5", "nome": "CAIO X SALVATORE", "sessione": "a5158e504228f90e28dea90693cccee1"};
                  break;
                default:
                  x = {"logged": false, "messaggio": "nome o password errati!"};
              }
            }
            break;
        case 1:
            {
                x = {"servizi": [{"id": "2108755", "giorno": "Sab 03 Dic", "tipo": ""}, {"id": "2108440", "giorno": "Ven 02 Dic", "tipo": ""}, {"id": "2107925", "giorno": "Gio 01 Dic", "tipo": ""}, {"id": null, "giorno": "Mer 30 Nov (RIP)", "tipo": "RIP"}, {"id": "2107185", "giorno": "Mar 29 Nov", "tipo": ""}, {"id": "2106785", "giorno": "Lun 28 Nov (MAL)", "tipo": "MAL"}, {"id": "2106516", "giorno": "Dom 27 Nov (MAL)", "tipo": "MAL"}, {"id": "2105807", "giorno": "Sab 26 Nov (MAL)", "tipo": "MAL"}, {"id": "2105454", "giorno": "Ven 25 Nov (MAL)", "tipo": "MAL"}]};
            }
            break;
        case 2:
            {
                x = {"details": {"id": "2108755", "giorno": "03\/12\/16", "tipo": "Servizio", "orario": "S", "a1": "733", "a2": "1", "a3": "15.12", "a4": "22.39", "a5": "PB", "a6": "R8", "b1": "", "b2": "0", "b3": "0.00", "b4": "0.00", "b5": "", "b6": "", "c1": "", "c2": "0", "c3": "0.00", "c4": "0.00", "c5": "", "c6": ""}};
            }
            break;

        default:
        {
            x = {"logged": false, "messaggio": "pagina non trovata!"};
        }

    }
    return callback(x);
}

/*$.mobile.loading('show', {
    text: "Connessione in corso...",
    textVisible: true,
    theme: "a",
    textonly: false
            //,html:
});*/
/*$.mobile.loading("hide");*/

/*
 url = 'http://intranet.amt.ct.it/tests/leggi_giorni.php?' + 'sessione=' + sessione;
 $.getJSON(url, function (json) {
 giorni = json.servizi;
 $.mobile.changePage($("#items"), "none");
 })
 */
