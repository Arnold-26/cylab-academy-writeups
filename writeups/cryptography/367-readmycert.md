# ReadMyCert

**Catégorie** : Cryptography · **Challenge** : #367 · **Résolu le** : 2026-11-23

## Énoncé

> How about we take you on an adventure on exploring certificate signing requests
> Take a look at this CSR file [here](https://challenge-files.cylabacademy.net/library/936e82e74aef68c1a8fcc80b032ea33d65adda1f04b5c46085d44a5d6ff7cb71/readmycert.csr).

## Résolution

Méthode : **openssl req -text**.

Le fichier est une **CSR** (Certificate Signing Request). `openssl req -in file.csr -noout -text` affiche le sujet, et le flag est dans le champ `CN`.

## Flag

```
academy{read_mycert_dcfb9c76}
```
