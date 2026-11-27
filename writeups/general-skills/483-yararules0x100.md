# YaraRules0x100

**Catégorie** : General Skills · **Challenge** : #483 · **Résolu le** : 2026-11-24

## Énoncé

> socat - TCP:xebec.cylabacademy.net:<port>

## Résolution

Méthode : **regle YARA soumise a un checker de 64 testcases (faux negatifs + faux positifs)**.

Le zip (mot de passe `picoctf`) contient `suspicious.exe`, un PE32 **compresse UPX** : `strings` ne donne rien tant qu'on ne le decompresse pas avec `upx -d` (26 624 -> 40 960 octets). Le binaire est un faux malware avec anti-debug, et l'enonce demande d'ecrire des regles YARA puis de les soumettre a un service (`socat - TCP:host:port`). Le protocole : envoyer le contenu de la regle puis fermer l'ecriture (EOF) ; le serveur teste la regle sur **64 cas** et rapporte separement les faux negatifs et les faux positifs. Pieges : un simple `condition: true` echoue en faux positif, et fermer la connexion trop vite apres l'envoi fait repondre « Your rulefile was empty » (il faut un court delai avant le shutdown). La regle gagnante combine le magic `{4D 5A}`, la chaine distinctive `YaraRules0x100`, `UPX`/`NtQuery`, et le motif large `debugger process`. Logique : exiger le magic PE plus un marqueur unique evite les faux positifs, tandis que la branche `$str5` couvre les variantes recompressees.

## Flag

```
academy{yara_rul35_r0ckzzz_790c7af6}
```

## Scripts

- [`solve.py`](../../solve/483/solve.py)
- *11 variantes intermediaires dans `solve/483/archive/`*
