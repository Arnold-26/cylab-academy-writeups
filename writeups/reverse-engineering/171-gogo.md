# gogo

**Catégorie** : Reverse Engineering · **Challenge** : #171 · **Résolu le** : 2026-11-25

## Énoncé

> enter_password (Go statique 32 bits) + service host:port

## Résolution

Méthode : **XOR de deux tableaux 32 octets + cassage MD5 de la seconde etape (ambush)**.

Binaire **Go statique 32 bits** avec ses symboles : `main.main`, `main.checkPassword`, `main.ambush`, `main.get_flag`. Etape 1 — `checkPassword` construit deux tableaux de 32 octets sur la pile puis les XOR : le premier est ecrit en `mov BYTE [esp+8+n]` (ASCII `861836f13e3d627dfa375bdb8389214e`), le second en **dwords little-endian** (`0x5d47534a`, `0x54034541`, `0x0a5a025d`, `0x0d455753`, `0x555d0005`, `0x0e011054`, `0x4b575541`, `0x01465045`). Le XOR des deux donne le mot de passe **`reverseengineericanbarelyforward`**. Piege important : recopier le second tableau a la main conduit a des erreurs — il faut convertir chaque dword avec `to_bytes(4, 'little')`. Etape 2 — le binaire ne va pas directement au flag : `main.main` appelle `main.ambush`, qui affiche « This challenge is interrupted by psociety / What is the unhashed key? ». Le desassemblage d'`ambush` montre un appel a `crypto/md5.Sum` suivi de la comparaison avec la meme chaine `861836f13e3d627dfa375bdb8389214e` : c'est donc un **MD5 a casser**. `john --format=raw-md5 --wordlist=rockyou.txt` le resout immediatement en **`goldfish`**. Verification locale avant d'attaquer le service : `printf 'reverseengineericanbarelyforward\ngoldfish\n' | ./enter_password` affiche `Flag is: academy{LOCAL_TEST_213}`, ce qui valide les deux entrees. `get_flag` lit alors `flag.txt` (visible dans les chaines du binaire) et imprime le drapeau. Sur le service, le format de l'adresse dans l'enonce est `host:port` sans `nc`, d'ou une regex adaptee.

## Flag

```
academy{p1kap1ka_p1c018269cc6}
```

## Scripts

- [`solve.py`](../../solve/171/solve.py)
- *12 variantes intermediaires dans `solve/171/archive/`*
