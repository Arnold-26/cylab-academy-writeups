# Wireshark doo dooo do doo...

**Catégorie** : Forensics · **Challenge** : #115 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **ROT13 dans un objet HTTP**.

Le pcap contient un objet HTTP `/` dont le corps est du texte en **ROT13** : `Gur synt vf npnqrzl{...}` se decode en `The flag is academy{...}`.

## Flag

```
academy{p33kab00_1_s33_u_deadbeef}
```

## Ce qu'il faut retenir

—
