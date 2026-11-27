# 714 — Rogue Tower

**Événement** : picoCTF 2026 · **Catégorie** : Forensics

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« A suspicious cell tower has been detected. » La capture `rogue_tower.pcap` doit permettre
d'identifier la tour pirate et de récupérer les données exfiltrées.

## Analyse
Malgré l'habillage cellulaire, le trafic utile est du **HTTP** ordinaire : un téléphone compromis
balise vers une « tour » pirate. L'identité de l'appareil (IMSI, CELL) voyage dans un en-tête
`User-Agent`, et le flag est exfiltré par morceaux en base64 dans le corps de plusieurs requêtes
`POST`. Le tout est chiffré par XOR avec une clé dérivée de l'IMSI.

Deux sources donnent des valeurs d'instance différentes (les captures sont régénérées) :
- une page de solution indique un `User-Agent` du type
  `MobileDevice/1.0 (IMSI:310410185261676; CELL:96261)` et une clé = les **8 derniers chiffres**
  de l'IMSI (`85261676`) ;
- un autre writeup mentionne un broadcast UDP (port 55000) annonçant `PLMN=00101`, `CELLID=91043`.

La méthode, elle, est stable : on repère la tour par le broadcast, on corrèle avec le `User-Agent`,
on reconstitue les segments base64, puis on casse le XOR par **known-plaintext** (`picoCTF{` en
début de clair) : les 8 octets obtenus doivent former une suite de chiffres, ce qui confirme que la
clé est bien la fin de l'IMSI.

## Solution
```bash
tshark -r rogue_tower.pcap -Y http -T fields -e http.host -e http.user_agent -e http.request.uri
tshark -r rogue_tower.pcap -Y 'http.user_agent contains "IMSI"' -T fields -e http.user_agent
tshark -r rogue_tower.pcap -Y 'http.request.method == "POST"' -T fields -e http.file_data
# concaténer les segments base64 DANS L'ORDRE des requêtes
```
Puis base64 → XOR avec la clé dérivée de l'IMSI (CyberChef `From Base64` → `XOR`, ou un script
Python). Si le XOR contre `picoCTF{` ne donne pas des chiffres, c'est que les segments ont été
concaténés dans le mauvais ordre ou que le mauvais découpage d'IMSI a été pris.

## Flag
```
picoCTF{r0gu3_c3ll_t0w3r_7a06fd7c}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-rogue-tower — page de solution picoCTF 2026 (IMSI/CELL, segments POST, XOR known-plaintext)
- https://cyb3r-bo1.github.io/posts/picoCTF_2026_writeup/ — writeup picoCTF 2026 (broadcast UDP, flag complet)
