# Milkslap

**Catégorie** : Forensics · **Challenge** : #139 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **LSB du canal bleu**.

Le sprite `concat_v.png` (1280x47520) contient le flag dans les **LSB du canal bleu**, des le premier pixel : `zsteg` plante sur une image aussi haute, il faut extraire les bits manuellement avec PIL + numpy.

## Flag

```
academy{imag3_m4n1pul4t10n_sl4p5}
```
