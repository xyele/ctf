# NOKTALAR TIRELER
Soruda bize aşağıdaki değer verilmişti.
```
MDAwIDAxIDEwIDEwMTAgMDEgMTAxIDEwIDExMSAxIDEwMDAgMDAgMTAgMDEgMDEwIDEwMTEgMDAgMSAwMDAgMTEgMTExIDAxMCAwMDAgMA==
```

Hemen Base64 ile decode ettim ve aşağıdaki binary değerine ulaştım.
```
000 01 10 1010 01 101 10 111 1 1000 00 10 01 010 1011 00 1 000 11 111 010 000 0
```

Soru başlığından faydalanarak `0` ile `.` ve `1` ile `-`yi replace ettirdim.
```
... .- -. -.-. .- -.- -. --- - -... .. -. .- .-. -.-- .. - ... -- --- .-. ... .
```

Daha sonra elde ettiğim değerin mors kodu olduğunu farkedip buradaki araç ile text değerini aldım.
```
sancaknotbinaryitsmorse
```

Flag
```
SANCAK{notbinaryitsmorse}
```