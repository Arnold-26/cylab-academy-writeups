# Classic Crackme 0x100

**Catégorie** : Reverse Engineering · **Challenge** : #409 · **Résolu le** : 2026-11-23

## Énoncé

> A classic Crackme. Find the password, get the flag!
>
> Binary can be downloaded [here](https://challenge-files.cylabacademy.net/library/f0eedad5a5dd920d309ff37bd28b097ed48e764e72b8720389eaa6e247a2bd18/crackme100).
>
> Crack the Binary file locally and recover the password. Use the same password on the server to get the flag!

## Résolution

Méthode : **inversion d'un Caesar par position**.

Le binaire construit une chaîne cible (movabs) puis applique 3 fois une transformation par caractère : un décalage de Cesar dont la valeur depend de l'indice (`((i%255)&0x55) + ((i%255)>>1 & 0x55)`, puis masque 0x33, puis 0x0f). Comme c'est un shift pur par position, on l'inverse en soustrayant 3*K. Piege : le dernier DWORD est écrit à l'offset 47 et ecrase un octet de la 6e chunk.

## Flag

```
academy{s0lv3_angry_symb0ls_08254898}
```
