# PowerAnalysis: Part 1

**Catégorie** : Cryptography · **Challenge** : #365 · **Résolu le** : 2026-11-25

## Énoncé

> Only a very limited number of measurements; traces.zip is provided.

## Résolution

Méthode : **cpa**.

`traces.zip` contient **100 fichiers** `traceNN.txt`, chacun avec son plaintext et sa
trace (format : `Plaintext: <hex>` puis `Power trace: [ ... ]`). Aucune requete reseau :
tout est hors ligne.

100 traces suffisent largement — la CPA sort les 16 octets avec 0,50 a 0,69 de correlation :

```
KEY: 40c457de8d13570387b99056bd9a17d1
```

Le piege est de croire qu'il faut « un nombre limite de mesures » pour ensuite interroger un
serveur : il n'y a pas de serveur, seulement l'archive.

### Le modele d'attaque

Chaque trace est une liste de 2666 entiers (la consommation du CPU pendant l'AES). L'attaque
est une **CPA** (correlation power analysis) sur le premier tour :

```
hypothese[k][t] = HammingWeight( Sbox[ plaintext[t][i] ^ k ] )
correlation    = corr( hypothese[k] , trace[:, t] ) pour chaque instant t
k_gagnant      = argmax_k  max_t |correlation|
```

C'est le modele classique « Hamming weight de la sortie de S-box ». Le bon octet de clef sort
avec une correlation de 0,5-0,7 contre 0,25-0,45 pour les suivants : la separation est nette,
inutile de monter a des milliers de traces.

Code (numpy, 20 lignes) :

```python
Tc = T - T.mean(axis=0); Tz = Tc / np.sqrt((Tc*Tc).sum(axis=0))
for i in range(16):
    H = HW[ SBOX[ P[:,i][None,:] ^ np.arange(256)[:,None] ] ]
    Hc = H - H.mean(axis=1, keepdims=True)
    corr = np.abs((Hc / np.sqrt((Hc*Hc).sum(axis=1, keepdims=True))) @ Tz)
    key[i] = corr.max(axis=1).argmax()
```

## Flag

```
academy{40c457de8d13570387b99056bd9a17d1}
```
