# ReadMyCert

**Catégorie** : Cryptography · **Challenge** : #367 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **openssl req -text**.

Le fichier est une **CSR** (Certificate Signing Request). `openssl req -in file.csr -noout -text` affiche le sujet, et le flag est dans le champ `CN`.

## Flag

```
academy{read_mycert_dcfb9c76}
```
