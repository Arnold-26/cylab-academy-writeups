# PowerAnalysis: Warmup

**Catégorie** : Cryptography · **Challenge** : #364 · **Résolu le** : 2026-11-25

## Énoncé

> Measure the power consumption of the CPU while it runs AES; leak the key.

## Résolution

Méthode : **cpa**.

Le service (`nc chatelaine.cylabacademy.net 42342`) accepte 16 octets de plaintext en
hex et renvoie une trace de puissance de 2666 points. **Une seule mesure par connexion** :
il faut rouvrir une socket a chaque trace.

Collecte : 300 plaintexts aleatoires (300 connexions, ~6 min), puis CPA.
Resultat : correlation 0,52-0,60 pour les 16 octets, 0,27 pour les dauphins.

```
KEY: ec1e6ecea34de3c3d1c81789bf49e482
```

Le flag est `academy{<cle hex minuscule>}` — le wrapper est `academy{}`, pas `picoCTF{}`.

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
academy{ec1e6ecea34de3c3d1c81789bf49e482}
```
