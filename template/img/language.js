var languages = {};


function loadLanguage() {

    var results = new RegExp('[\?&]' + 'lang' + '=([^&#]*)').exec(window.location.href);
  
    if (results == null) {
        var value =  "pt";

        
    $.getJSON('/template/'+value+".json", function(result) {
        languages = result;
        
        
        
            if (value == "pt"){ 
            	renderToLanguage("Portuguese", value);
            	$("#selectLanguage").val("portuguese");

            }        
        
        $("body").removeClass("hideText");

    }).fail(function(e){
        $("body").removeClass("hideText");
    });
    }else{
        $("#selectLanguage").val("english");
        $("body").removeClass("hideText");
    }
}

function changeLanguage(lang) {
    var langCode;

    if (lang == "english") langCode = "en";
        var url = window.location.href;
    if (url.indexOf('?') != -1) url = url.substring(0, url.indexOf('?'));
    if (lang != "portuguese") {
        url = url + "?lang=" + langCode;
        window.location.href = url;
        window.language = 'en';
        renderToLanguage(lang, langCode);
        $("#selectLanguage").val("english");
    } else {
        window.location=url;
    }

}

function renderToLanguage(lang, langCode) {
    window.language=lang;
    var choosenLang = languages[lang];
    $("html").attr("lang", langCode);
    $("[data-lang-entry]").each(function(i, e) {
        var entry = $(e).attr("data-lang-entry");
        $(e).text(choosenLang[entry]);
    })    
    $("input[data-lang-entry]").each(function(i,e){
        var holder=$(e).attr("data-lang-entry");
        $(e).attr("placeholder", choosenLang[holder]);
    })  
    $("textarea").each(function(i,e){
        var holder=$(e).attr("data-lang-entry");
        $(e).attr("placeholder", choosenLang[holder]);
    }) 
    $("input[type='submit'][data-lang-entry]").each(function(i,e){
    var holder=$(e).attr("data-lang-entry");
    $(e).attr("value", choosenLang[holder]);
    }) 
}

