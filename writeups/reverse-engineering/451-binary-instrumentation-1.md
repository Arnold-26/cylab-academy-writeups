# 451 — Binary Instrumentation 1 — Reverse Engineering

**Catégorie** : Reverse Engineering · **Challenge** : #451 · **Événement** : picoCTF 2025

## Énoncé

> I have been learning to use the Windows API to do cool stuff! Can you wake up my program to get the flag?
>
> Download the exe [here](https://challenge-files.cylabacademy.net/library/b707862077450010bce3c050b139b7c00762859eb94eea5db8eded717a6318d0/bininst1.zip). Unzip the archive with the password `academy`

**Flag :** `academy{w4ke_m3_up_w1th_fr1da_f27acc38}`
**Fichier :** `bininst1.zip` (mdp `academy`) → `bininst1.exe` (PE32+ x86-64, 462 848 o).
**Énoncé :** *« I have been learning to use the Windows API to do cool stuff! Can you wake up my
program to get the flag? »* — indices : Frida, `frida-trace`.

## Le binaire est packé — et ça se dépacke à la main

Recon : `.text` fait seulement 0x46F0 (18 Ko) et commence par du **code leurre** (appels d'API avec
des arguments NULL, `GetLastError` comparé à 0x361c), tandis qu'une section **`.ATOM` de 437 Ko** à une **entropie de 8.00** (chiffrée/compressée). Les deux challenges 451 et 452 partagent d'ailleurs
un `.text` identique : seule la charge utile diffère.

Le désassemblage de la plus grosse fonction (`0x140002840`, 3464 o) montre le **range coder LZMA**
caractéristique (`>> 11`, `imul` sur une table de probabilités, `0x800`, `- (p >> 5)`) : c'est un
`LzmaDec`. Et le début de `.ATOM` :

```
5d 00 00 10 00  65 99 23 00 00 00 00 00 ...
```

`0x5d = 93 = (2*5+0)*9 + 3` → **lc=3, lp=0, pb=2**, dictionnaire `0x00100000` (1 Mo), puis la taille
décompressée sur 8 octets (`0x239965` = 2 333 029). C'est **exactement l'en-tête `.lzma` « alone »**
(5 o de props + 8 o de taille) : inutile d'écrire un unpacker, `lzma.FORMAT_ALONE` suffit.

```python
blob = section('.ATOM')                     # 437 Ko
out  = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(blob)
# -> 2 333 029 octets, et out[:2] == b'MZ'  =>  c'est un PE !
```

Le payload est un PE32+ de 2,3 Mo (19 sections, `.text` de 0xb39f8) : le vrai programme.

## Le flag

Dans le payload décompressé, une simple passe `strings` donne :

```
Hi, I have the flag for you just right here!
Ok, I'm Up! The flag is: YWNhZGVteXt3NGtlX20zX3VwX3cxdGhfZnIxZGFfZjI3YWNjMzh9
```

Le flag est encodé en base64 → `academy{w4ke_m3_up_w1th_fr1da_f27acc38}`.

Un scan systématique des chaînes base64 du payload confirme (et évite de rater une variante) :
`_z_bi_b64.py` décode toutes les runs `[A-Za-z0-9+/]{16,}` et cherche `academy{`.

## Pourquoi l'exécution directe est impossible ici

Windows **bloque le lancement** du stub packé (Defender : « le fichier contient un virus »), et
`wine` sur le stub crashait déjà (page fault à l'image base) — signature classique d'un packer.
Le dépackage statique est donc la bonne voie, et il rend l'énoncé Frida inutile.

## Scripts

- [`solve.py`](../../solve/451/solve.py)
