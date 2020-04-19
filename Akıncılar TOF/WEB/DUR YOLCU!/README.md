# DUR YOLCU!
![](1.png)
Verilen web sayfasına girdiğimde karşıma `GIRIŞ YAP` ve `KAYIT OL` yazan iki panel çıktı. Öncelikle kayıt olup hesabımla giriş yaptım ancak karşıma veri girişi yapamayacağım bir web sayfasına yönlendirdi.
![](2.png)
`ÇANAKKALE HAKKINDA` linkine tıkladığımda ise [Çanakkale Savaşı Wikipedia Sayfası](https://tr.wikipedia.org/wiki/%C3%87anakkale_Sava%C5%9F%C4%B1)na yönlendiriyordu.
Birkaç denemeden sonra kullanıcı adıma `'` (tırnak) ekleyerek bir login isteği gönderdiğimde karşıma `SQL syntax hatası` çıktı.
![](3.png)
Daha sonra web isteğini hemen `Burp Suite` ile yakalayıp bir dosyaya kaydettim.
![](4.png)
Ardından aydettiğim isteği `-r` parametresi ile `SQLMap` aracına verdim.
![](5.png)
Ve sırayla birkaç komut ardından veritabanındaki kayıtları elde etmek için gerekli komutu çalıştırdım. Flag `Users` tablosundaki ilk kaydın `Password` colomnundaydı.
![](6.png)
Böylece aşağıdaki komutla flagi elde etmiş oldum.
```
sqlmap -r duryolcu.req -D Canakkale -T Users -C ID,Username,Password --dump
```

Flag
```
SANCAK{Canakkale_1_SQLi_ile_Gecilmez}
```