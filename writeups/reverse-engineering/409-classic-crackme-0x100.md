# Classic Crackme 0x100

**Catégorie** : Reverse Engineering · **Challenge** : #409 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **inversion d'un Caesar par position**.

Le binaire construit une chaine cible (movabs) puis applique 3 fois une transformation par caractere : un decalage de Cesar dont la valeur depend de l'indice (`((i%255)&0x55) + ((i%255)>>1 & 0x55)`, puis masque 0x33, puis 0x0f). Comme c'est un shift pur par position, on l'inverse en soustrayant 3*K. Piege : le dernier DWORD est ecrit a l'offset 47 et ecrase un octet de la 6e chunk.

## Flag

```
academy{s0lv3_angry_symb0ls_08254898}
```

## Ce qu'il faut retenir

—
