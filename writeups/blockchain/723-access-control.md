# Access_Control

**Catégorie** : Blockchain · **Challenge** : #723 · **Résolu le** : 2026-11-24

## Énoncé

> eth node xebec.cylabacademy.net:<port>

## Résolution

Méthode : **fonction changeOwner sans controle d'acces**.

Contrat Solidity 0.8 avec une fonction `changeOwner(address)` declaree **`public` sans aucun controle d'acces** (pas de `onlyOwner`) : n'importe qui peut s'attribuer la propriete, puis appeler `solve()` qui exige `msg.sender == owner` et declenche `FlagRevealed`. Deux transactions suffisent : `changeOwner(<mon adresse>)` puis `solve()`, et `getFlag()` renvoie le secret. Point technique : le noeud n'expose pas de compte deverrouille, il fallait donc signer soi-meme. J'ai ecrit `ethlight.py` : keccak-256 (pycryptodome), RLP, et ECDSA secp256k1 en Python pur, avec signature legacy EIP-155 (`v = recid + 35 + 2*chainId`, normalisation low-s et bascule du recid). Verification : l'adresse derivee de la cle privee correspond exactement a celle du joueur, ce qui valide l'implementation avant d'envoyer quoi que ce soit.

## Flag

```
academy{i_c4n_b3_0wn3r_7a45d669}
```

## Ce qu'il faut retenir

—
