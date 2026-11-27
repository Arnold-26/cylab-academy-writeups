# Tap into Hash

**Catégorie** : Reverse Engineering · **Challenge** : #466 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **dechiffrement XOR du blockchain**.

`block_chain.py` chiffre une chaine de hashes de blocs par XOR repetitif avec `sha256(key)[:16]`, apres y avoir insere le flag au milieu. Le fichier `enc_flag` donne la cle et le chiffre : un XOR avec `sha256(key)[:16]` puis depadding PKCS#7 revele le flag au milieu de la chaine de hashes.

## Flag

```
academy{block_3SRhViRbT1qcX_XUjM0r49cH_qCzmJZzBK_d61a533f}
```

## Ce qu'il faut retenir

—
