# college-rowing-team

**Catégorie** : Cryptography · **Challenge** : #212 · **Résolu le** : 2026-11-23

## Énoncé

> I just joined my college's rowing team! To make a good first impression, I started sending my teammates positive automated messages every day. I even send them flags from time to time!

## Résolution

Méthode : **petit exposant + racine cubique**.

`e = 3` et le message est court : `m^3 < n`, donc le chiffre est exactement `m^3` sans reduction modulaire. Une simple racine cubique entiere redonne le clair pour chacun des 12 messages.

## Flag

```
picoCTF{1_gu3ss_p30pl3_p4d_m3ss4g3s_f0r_4_r34s0n}
```
