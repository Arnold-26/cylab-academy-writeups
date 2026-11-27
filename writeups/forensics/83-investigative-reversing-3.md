# Investigative Reversing 3

**Catégorie** : Forensics · **Challenge** : #83 · **Résolu le** : 2026-11-25

## Énoncé

> investigative-reversing-3-mystery + investigative-reversing-3-encoded.bmp

## Résolution

Méthode : **LSB après 723 octets, pas de 9 octets par caractère (mesure par double exécution)**.

Même famille que 13 : le binaire `investigative-reversing-3-mystery` (PIE, non strippe) recopie **723 octets** (`0x2d3`) d'en-tete, puis appelle `codedChar(j, flag[i/2], octet)` pour 100 groupes de 8 bits. `codedChar` écrit le bit dans le **LSB** : `(octet & 0xfe) | ((ch >> bit) & 1)`. Le piege est la disposition : au lieu d'un bloc contigu de 8 octets par caractère, chaque caractère occupe un **pas de 9 octets** (8 bits + 1 octet de gap), donc le bit j du caractère k est le LSB de l'octet `723 + 9*k + j`. **Méthode qui a permis de le prouver** : exécuter le binaire deux fois avec des drapeaux connus dont tous les bits different (`'A'*50` = 0x41 puis `'B'*50` = 0x42, qui ne different que par les bits 0 et 1), puis differ les deux images produites. On obtient exactement **100 octets modifies**, par paires aux offsets 723/724, 732/733, 741/742... : le pas 9 et la largeur 1 octet par bit sont ainsi mesures directement sur le binaire, sans supposition. L'extraction avec ce pas donne `academy{4n0th3r_L5b_pr0bl3m_00000000000001eb97d9c}`. Lecon : quand l'analyse statique ne tranche pas, faire tourner le binaire sur des entrées controlees et differer les sorties est plus rapide et plus sur que de deviner la disposition.

## Flag

```
academy{4n0th3r_L5b_pr0bl3m_00000000000001eb97d9c}
```

## Scripts

- [`solve.py`](../../solve/83/solve.py)
