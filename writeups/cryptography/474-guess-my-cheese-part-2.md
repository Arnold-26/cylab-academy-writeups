# Guess My Cheese (Part 2)

**Catégorie** : Cryptography · **Challenge** : #474 · **Résolu le** : 2026-11-25

## Énoncé

> The imposter fooled us last time, so we strengthened our defenses!

## Résolution

Méthode : **hash salt brute force**.

Le service (`nc` sur l'instance) affiche un SHA-256 (64 hex), puis demande
« what's my cheese? » puis « what's my salt? ».

### Le piege : le sel change a chaque connexion

Chaque nouvelle connexion affiche un hash different. Il faut donc brute-forcer **dans la meme
connexion** : le serveur attend la reponse, on calcule (~3 s), on repond.

### Construction exacte du hash (verifiee par l'experience)

```
sha256( cheese.lower() + chr(salt_byte) )
```

Attention a trois details qui coutent des heures si on les rate :

1. **le fromage est mis en minuscules** dans le hash (`Butterkase` -> `butterkase`) ;
2. le sel est **un seul octet brut** (pas une chaine hex) ajoute au nom ;
3. a la question « what's my salt? » il faut repondre **la representation hexadecimale sur
   2 caracteres** (`0x54` -> `54`), pas le caractere.

### Script

```python
for c in cheeses:                      # 599 noms de cheese_list.txt
    for sb in range(256):
        if sha256((c.lower() + chr(sb)).encode()).hexdigest() == target:
            found = (c, sb)
```

Puis : `g`, le nom **d'origine** (`Butterkase`), puis `"%02x" % sb` (`54`).

Reponse du serveur :

```
   _   _
  (q\_/p)  ...
MUNCH.............
academy{cHeEsY1e5a870a}
```

### A retenir

- Un hash qui change a chaque connexion n'est pas forcement hors de portee : si l'entropie du
  sel est faible (1 octet), l'espace `599 x 256` se parcourt en 3 secondes — mais **il faut
  rester dans la session**.
- Les animations du service (`munch...`, `BLEHHHHH yuck. THAT'S not my cheese`) sont des
  oracles : « yuck » = fromage faux, `munch` sans verdict = fromage bon mais sel mal formatte.
  C'est ce qui a revele qu'il fallait envoyer le sel en hex.
- Verifier la **casse** : le hash utilise `lower()`, la comparaison du nom attend la casse
  d'origine.

## Flag

```
academy{cHeEsY1e5a870a}
```

## Scripts

- [`solve.py`](../../solve/474/solve.py)
- *13 variantes intermediaires dans `solve/474/archive/`*
