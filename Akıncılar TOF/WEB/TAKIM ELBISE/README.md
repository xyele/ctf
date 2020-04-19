# TAKIM ELBISE
Verilen web sayfasına girdiğimde karşımda Cem Yılmazın oynadığı Vizontele filminden alıntılarla karşılaştım :)
![](1.png)
Aşağıdaki linke tıkladığımda `?kaynak` hedefine yönlendiriyordu ve orada ise sayfanın kaynak kodu bizi karşılıyordu.
```PHP
<!DOCTYPE HTML>
<?php
  require("sancak.php");

  if (isset($_GET['kaynak'])) {
    highlight_file(__FILE__);
    die();
  }

  if (isset($_GET['emin'])) {

    $ne_dedi_ne_dedi = $_GET['emin'];
    $neyi_duymak_istemiyorsun = 'takimelbise';
    $sende_bunu_yedin = preg_replace(
            "/$neyi_duymak_istemiyorsun/", '', $ne_dedi_ne_dedi);

    if ($sende_bunu_yedin === $neyi_duymak_istemiyorsun) {
      sen_iceri_gec_iceri();
    }
  }
?>

<html>
  <head>
    <title>Takım Elbise</title>
  </head>
  <body>
    <h1>Yok ben söylerim çayı</h1>
    <p>Sen içeri geç içeri...</p>
    </div>
    <img src="fikri.jpg">
    <div>
    <a target="_blank" href="?kaynak">Kaynak kodu gör.</a>
  </body>
</html>

```