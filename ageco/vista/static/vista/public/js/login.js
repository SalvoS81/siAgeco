/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


function LogData() {
    'use strict';
    this.logged = false;
    this.versione = "";
    this.distintivo = "";
    this.nome = "";
    this.sessione = "";
    this.matricola = "";
    this.password = "";
    this.rimaniconnesso = false;
}

var chi = new LogData();
var servizi;

$(document).ready(function () {

    'use strict';
    inizializza();

    $('#bt_registra').click(function() {
            mostra_login_ad();
            start_ad_help();
    });
    $('#bt_home').click(function() {
            $("#login-box-msg").show();
            $("#login-box-msg_ad").hide();
            $("#bt_vai").hide();
            $("#bt_home").hide();
            $("#bt_registra").show();
            $("#login_form").show();
            $("#login_form_ad").hide();
            $("#agenda_login_help").hide();
    });

    $("#login_form_ad").submit(function (event) {
        $("#msgbox").removeClass().addClass('messagebox').text("Verifica credenziali nell'Area Dipendenti....").fadeIn(1000);
        var userField = $("#username_ad").val();
        var pwdField = $("#password_ad").val();
        var url = url_intranet + 'user=' + userField + '&password=' + pwdField;
        //messaggio("<b>debug:</b> "+"Mi collego a " + url);
        //$.getJSON(url, function (risp){
        myGetJSON(url, function (risp) {
            //mostraStruttura("<b>debug:</b> "+"Risposta Server", risp);
            if (risp.logged) {
              chi.logged = risp.logged;
              chi.versione = risp.versione;
              chi.distintivo = risp.distintivo;
              chi.nome = risp.nome;
              chi.sessione = risp.sessione;
              chi.matricola = $("#username_ad").val();
              chi.password = $("#password_ad").val();
              chi.rimaniconnesso = $("#remember_me_ad").is(":checked");
              //mostraStruttura("<b>debug:</b> "+"Chi ", chi);
              var chiJSON = JSON.stringify(chi);
              //messaggio("<b>debug:</b> "+chiJSON);
              localStorage.setItem("logDataSalvato", chiJSON );
              messaggio("Registrato come: " + chi.distintivo);
              //$("#msgbox").removeClass().addClass('messagebox').text("Validazione...").fadeIn(2000);
              //ORIGINALE
              $("#msgbox").fadeTo(200,0.1,function()  //start fading the messagebox
              {
                //var url = '/agenda/registrazione' ;//+ 'logresult=' + chiJSON;
                messaggio("Registrazione credenziali utente in corso... " /*+ "<b>debug:</b> " + url_registrazione*/);
                $(this).html('Registrazione in corso.....').addClass('messageboxok').fadeTo(1000,1, function()
                {
                  $.post(url_registrazione, chiJSON)
                    .done(function(data){
                      messaggio(data);
                      $("#msgbox").fadeTo(200,0.1,function()  //start fading the messagebox
                      {
                        //var url = '/agenda/login';
                        messaggio("Effettuo l'accesso...");
                        $(this).html('Autenticazione in corso.....').addClass('messageboxok').fadeTo(1000,1, function()
                        {
                          $.post(url_login, { "_username" : chi.matricola, "_password" : chi.password, "_remember_me" : chi.rimaniconnesso})
                            .done(function(){
                              messaggio("Reindirizzamento...");
                              $(location).attr('href', url_homepage);
                              //window.location = data.location;
                            });
                        });
                      });
                    });
                });
              });
            } else {
                localStorage.removeItem("logDataSalvato");
                $("#msgbox").fadeTo(200,0.1,function() //start fading the messagebox
                {
                    //add message and change the class of the box and start fading
                    $(this).html("Matricola o pin errati...<br>Se non ricordi il pin vai all'area dipedenti per recuperarlo.").addClass('messageboxerror').fadeTo(900,1);
                });
            }
        });

        event.preventDefault();
    });
});
function mostra_login_ad(){
    $("#login-box-msg").hide();
    $("#login-box-msg_ad").show();
    $("#bt_vai").show();
    $("#bt_home").show();
    $("#bt_registra").hide();
    $("#login_form").hide();
    $("#login_form_ad").show();
    $("#agenda_login_help").show();
}
function start_ad_help(){
    clearMessaggio();
    //messaggio("<b>debug:</b> "+url_homepage+" "+url_registrazione+" "+url_login);
    messaggio(
      "Per accedere ad <b>Agenda Conducente</b> registra qui la matricola e il pin dell'Area Dipendenti Amt."+
      "<br>Se non ricordi il Pin, segui questi semplici passaggi: "+
      "<ul><li>Clicca su Esci e Vai all'area dipendeti. </li>"+
      "<li>Clicca su Pin smarrito ed esegui i passaggi suggeriti.</li>"+
      "<li>Riapri Agenda Conducente ed inserisci la matricola e il nuovo pin.</li></ul>");
    messaggio("Recupero credenziali...");
    setTimeout(function () {
        if (chi.logged) {
            //mostraStruttura("<b>debug:</b> "+"Chi ", chi);
            messaggio("Bentornato, " + chi.nome);
            $("#username_ad").val(chi.matricola);
            $("#password_ad").val(chi.password);
            if (chi.rimaniconnesso === true) { $('input').iCheck('check'); }
            else { $('input').iCheck('uncheck'); }
            messaggio("Inserisci il pin e premi <b>Registra ed Entra</b> per effettuare l'accesso!");
        } else {
          messaggio("Non presenti!<br>Inserisci le credenziali e premi <b>Entra</b>.");
        }
    }, 1000);
}
function inizializza(){
    chi = JSON.parse(localStorage.getItem("logDataSalvato")) || chi;
    if (!chi.logged) {
      mostra_login_ad();
      start_ad_help()
    }else{
      $("#username").val(chi.matricola);
      //$("#password").val(chi.password);
    }
}

function mostraStruttura(cosa, quale) {
    messaggio(" INIZIO------- " + cosa + " ---------- ");
    $.each(quale, function (i, field) {
        if (!(typeof field === "function")) {
            messaggio("|-- " + [i] + " : " + field);
        }
    });
    messaggio(" FINE------- " + cosa + " ---------- ");
}
function messaggio(msg) {
    var x = $("#txt_comunicazioni").html();
    $("#txt_comunicazioni").html(x + "<br>" + msg);
    //console.log(msg);
}
function clearMessaggio() {
    $("#txt_comunicazioni").html("<b>Benvenuto!</b>");
}
