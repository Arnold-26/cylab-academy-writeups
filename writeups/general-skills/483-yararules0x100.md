# YaraRules0x100

**Catégorie** : Général Skills · **Challenge** : #483 · **Résolu le** : 2026-11-24

## Énoncé

> socat - TCP:xebec.cylabacademy.net:<port>

## Résolution

Méthode : **regle YARA soumise à un checker de 64 testcases (faux négatifs + faux positifs)**.

Le zip (mot de passe `picoctf`) contient `suspicious.exe`, un PE32 **compresse UPX** : `strings` ne donne rien tant qu'on ne le decompresse pas avec `upx -d` (26 624 -> 40 960 octets). Le binaire est un faux malware avec anti-debug, et l'énoncé demande d'écrire des regles YARA puis de les soumettre à un service (`socat - TCP:host:port`). Le protocole : envoyer le contenu de la regle puis fermer l'écriture (EOF) ; le serveur teste la regle sur **64 cas** et rapporte separement les faux négatifs et les faux positifs. Pieges : un simple `condition: true` échoue en faux positif, et fermer la connexion trop vite après l'envoi fait répondre « Your rulefile was empty » (il faut un court delai avant le shutdown). La regle gagnante combine le magic `{4D 5A}`, la chaîne distinctive `YaraRules0x100`, `UPX`/`NtQuery`, et le motif large `debugger process`. Logique : exiger le magic PE plus un marqueur unique evite les faux positifs, tandis que la branche `$str5` couvre les variantes recompressees.

## Flag

```
academy{yara_rul35_r0ckzzz_790c7af6}
```

## Scripts

- [`solve.py`](../../solve/483/solve.py)
