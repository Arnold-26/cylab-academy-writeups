# advanced-potion-making

**Catégorie** : Forensics · **Challenge** : #205 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **en-tete PNG + plan LSB**.

Le fichier a un en-tete PNG corrompu (`89 50 42 11 ...` au lieu de `89 50 4E 47 ...` + longueur IHDR). Une fois les 12 premiers octets restaures (tous les CRC sont alors valides), l'image est un aplat rouge. Le **plan LSB du canal rouge** dessine le flag en blanc sur noir.

## Flag

```
picoCTF{w1z4rdry}
```

## Ce qu'il faut retenir

—
