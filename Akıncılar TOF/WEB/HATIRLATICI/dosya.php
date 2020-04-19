$value = time();
$dosyaadi = $_GET["dosyaadi"];
$erisimkodu = $_GET["erisimkodu"];
if (base64_encode(md5($dosyaadi)) == $erisimkodu){
echo "Erisim basarili => $dosyaadi!

";
srand($value);
if (in_array($dosyaadi, array('dosya.php', 'index.html', 'key.txt', 'sifreler.txt', 'kullanicilar.txt'))==TRUE){
$veri = file_get_contents($dosyaadi);
if ($veri !== TRUE) {
if ($dosyaadi == "key.txt") {
$anahtar = $_GET["anahtar"];
if (md5(base64_encode(md5($dosyaadi))) == $anahtar){
$veri = file_get_contents("onemlinotlar.txt");
echo ($veri);
}
}
else{
echo nl2br($veri);
}

}
else{
echo nl2br($veri);
}
}
else{
echo "Dosya mevcut degil";
}

}
else{
echo "Gecersiz erisim kodu";
}
?>