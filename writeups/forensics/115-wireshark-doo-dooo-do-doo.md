# Wireshark doo dooo do doo...

**Catégorie** : Forensics · **Challenge** : #115 · **Résolu le** : 2026-11-23

## Énoncé

> Can you find the flag?
> [shark1.pcapng](https://challenge-files.cylabacademy.net/library/e43f1616b24c48529987bf5cce4c1c835cabce4dee3c80db64593dc0ef11d8d5/shark1.pcapng)

## Résolution

Méthode : **ROT13 dans un objet HTTP**.

Le pcap contient un objet HTTP `/` dont le corps est du texte en **ROT13** : `Gur synt vf npnqrzl{...}` se decode en `The flag is academy{...}`.

## Flag

```
academy{p33kab00_1_s33_u_deadbeef}
```
