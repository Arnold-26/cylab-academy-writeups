# Tap into Hash

**Catégorie** : Reverse Engineering · **Challenge** : #466 · **Résolu le** : 2026-11-23

## Énoncé

> Can you make sense of this source code file and write a function that will decode the given encrypted file content?
> Find the encrypted file [here](https://challenge-files.cylabacademy.net/library/e6633c386f37056f8c7173364a60cd48236fb1e99e10556725ec2c0c39614e02/enc_flag). It might be good to analyze [source file](https://challenge-files.cylabacademy.net/library/e6633c386f37056f8c7173364a60cd48236fb1e99e10556725ec2c0c39614e02/block_chain.py) to get the flag.

## Résolution

Méthode : **déchiffrement XOR du blockchain**.

`block_chain.py` chiffre une chaîne de hashes de blocs par XOR repetitif avec `sha256(key)[:16]`, après y avoir insere le flag au milieu. Le fichier `enc_flag` donne la clé et le chiffre : un XOR avec `sha256(key)[:16]` puis depadding PKCS#7 révèle le flag au milieu de la chaîne de hashes.

## Flag

```
academy{block_3SRhViRbT1qcX_XUjM0r49cH_qCzmJZzBK_d61a533f}
```
