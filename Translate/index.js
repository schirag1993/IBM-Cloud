var express     = require('express'),
    app         = express(),
    request     = require('request'),
    bodyParser  = require('body-parser'),
    // config    = require('./config.json'),
    methodOverride = require('method-override');

var LanguageTranslatorV2 = require('watson-developer-cloud/language-translator/v2');

var languages = [{"language":"English","langCode":"en"}, {"language":"Arabic","langCode":"ar"},
                  {"language":"French","langCode":"fr"}, {"language":"German","langCode":"de"}, {"language":"Italian","langCode":"it"},
                  {"language":"Japanese","langCode":"ja"}, {"language":"Portuguese","langCode":"pt"}, {"language":"Korean","langCode":"ko"},
                  {"language":"Spanish","langCode":"es"}]

app.use(bodyParser.urlencoded({extended: true}));
app.set('view engine', 'ejs');

app.get('/', function(req,res) {
  if(req.query.translateOutput) {
    console.log(req.query.translateOutput);
    res.render("success", {translated:req.query.translateOutput});
  }
  else {
    res.render('home', {languages:languages});
  }
});

app.post('/translate', function(req,res){
  console.log(JSON.stringify(req.body));
  ibmCreds = {
    "username" : req.body.username,
    "password" : req.body.password,
    "url" : req.body.url
  };
  textData = {
    "fromLang" : req.body.fromLang,
    "toLang" : req.body.toLang,
    "textToConvert" : req.body.textToConvert
  };
  convertText(ibmCreds, textData, function(err, answer) {
    if(err) {
      console.log("Error: " + err);
      res.redirect("error")
    }
    else {
      console.log("Success!");
      console.log(answer.translations[0].translation);
      res.redirect("/?translateOutput=" + answer.translations[0].translation)
    }
  });
})

app.listen(8080, function() {
    console.log('Connected. Listening on port number: ' + 8080)
})

function convertText(ibmCreds, textData, callback) {
  var language_translator = new LanguageTranslatorV2({
    username: ibmCreds.username,
    password: ibmCreds.password,
    url: ibmCreds.url
  });
  language_translator.translate(
  {
    text: textData.textToConvert,
    source: textData.fromLang,
    target: textData.toLang
  },
  function(err, translation) {
    if (err)  {
      console.log('error:', err);
      callback(true, null);
    } else  {
      console.log(JSON.stringify(translation, null, 2));
      callback(null, translation)
  }
});
}
