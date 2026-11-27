# 452 — Binary Instrumentation 2 — Reverse Engineering

**Catégorie** : Reverse Engineering · **Challenge** : #452 · **Événement** : picoCTF 2025

## Énoncé

> I've been learning more Windows API functions to do my bidding. Hmm... I swear this program was supposed to create a file and write the flag directly to the file. Can you try and intercept the file writing function to see what went wrong?
>
> Download the exe [here](https://challenge-files.cylabacademy.net/library/ce8f745beda824c87d5482c853c90b7758b9a95d9b05db0c74fb2b0678f8115b/bininst2.zip). Unzip the archive with the password `academy`

**Flag :** `academy{fr1da_f0r_b1n_in5trum3nt4tion!_b21aef39}`
**Fichier :** `bininst2.zip` (mdp `academy`) → `bininst2.exe` (PE32+ x86-64, 462 336 o).
**Énoncé :** *« I swear this program was supposed to create a file and write the flag directly to
the file. Can you try and intercept the file writing function to see what went wrong? »*

## Même packer que 451 → même dépackage

`bininst2.exe` est le **même stub** que `bininst1.exe` (section `.text` identique) avec une charge
utile LZMA différente :

```
.ATOM : 5d 00 00 10 00 | 1e 94 23 00 00 00 00 00   (lc=3 lp=0 pb=2, dict 1 Mo, 2 331 678 o)
```

Donc, comme pour 451 : `lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(.ATOM)`
→ PE32+ de 2,3 Mo (`bininst2_payload.bin`), écrit par `_z_bi_unlzma.py`.

## Le flag

Le payload est un binaire C++ (chaînes `basic_filebuf`, `random_device`, `VirtualProtect failed…`).
Le flag y est stocké en **base64** ; `_z_bi_b64.py` (scan de toutes les runs base64 puis recherche
de `academy{`) le sort directement :

```
YWNhZGVteXtmcjFkYV9mMHJfYjFuX2luNXRydW0zbnQ0dGlvbiFfYjIxYWVmMzl9
-> academy{fr1da_f0r_b1n_in5trum3nt4tion!_b21aef39}
```

Aucune instrumentation n'était nécessaire : le programme écrit bien le flag dans un fichier, mais
la chaîne est en clair (encodée base64) dans le binaire — l'interception `WriteFile` de l'énoncé
n'aurait fait que confirmer.

## Notes

- Les deux challenge partagent le stub : `_z_bi_pe.py` montre un `.text` de 0x46f0 identique et une
  section `.ATOM` à entropie 8.00 dans les deux cas.
- Windows refuse de lancer les stubs (Defender) et `wine` crashe dessus : le dépackage statique est
  la seule voie, et il est trivial grâce à l'en-tête LZMA standard.

## Scripts

- [`solve.py`](../../solve/452/solve.py)
- *7 variantes intermediaires dans `solve/452/archive/`*
