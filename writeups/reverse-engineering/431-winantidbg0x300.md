# 431 — WinAntiDbg0x300 — Reverse Engineering

**Flag :** `academy{Wind0ws_antid3bg_0x300_f57a6e29}`
**Artefacts :** `WinAntiDbg0x300.exe` (PE32 **packé UPX**, 26 624 o), `WinAntiDbg0x300.pdb`
(880 640 o), `config.bin` (86 o) — zip protégé par `academy`.

## Dépacker d'abord (sinon le .pdb ne sert à rien)

```
rabin2 -S WinAntiDbg0x300.exe     # sections UPX0/UPX1
upx -d WinAntiDbg0x300.exe -o u300.exe   # 75 264 o, .text @ 0x401000
```

Les adresses du `.pdb` (`ReadConfig`, `DecryptFlag`, `DetectDebuggerAtLaunch`, `CONFIG_BUFFER`,
`FLAG`, `FLAG_SIZE`) sont celles du binaire **dépacké** — d'où les zéros au premier essai sur le
binaire packé.

## Le dispatch CFG du packer

Entre `0x4011f0` et `0x4012a0` ce ne sont pas des appels mais une **table de `jmp`** ; un thunk
`v` se résout par `cible = v + 5 + int32(bytes[v+1:v+5])` :

```
0x401073 -> 0x402b30  (affichage : MultiByteToWideChar CP_UTF8 + fwrite)
0x4011e0 -> 0x402e00
0x40122b -> 0x402bc0  (mutate)
0x40127b -> 0x402cb0  (DecryptFlag)
```

## Flux reconstitué

1. `ReadConfig` (`0x402980`) : `GetModuleFileNameA` → répertoire de l'exe → `config.bin`.
   Lit `[u32 size]` puis `2*size+2` octets, exige `size < 200` et `n == 2*size+2`.
   `CONFIG_BUFFER` (0x40c3d0) = le bloc de 200 o, `FLAG_SIZE` (0x40c3d8) = size,
   `FLAG` (0x40c3d4) = `CONFIG_BUFFER + size + 1`.
2. `mutate(1)` (`0x402bc0`) sur `CONFIG_BUFFER[0..size-1]`.
3. `DecryptFlag(CONFIG_BUFFER)` (`0x402cb0`) : `FLAG[i] ^= CONFIG_BUFFER[i]`.
4. `0x4038e0` : affichage, puis `fwrite`.

## `mutate` — attention, `ch` ne bouge pas

```c
buf[j] = 'a' + (((buf[j] - 'a') + popcount(j % 255)) % 26);
```
`popcount` est calculé par la triade `&0x55 / &0x33 / &0x0f` ; `ch = 0x61` est chargé une fois
en `[ebp-1]` et **n'est jamais réécrit** (le seul `mov [reg], cl` écrit dans `buf[j]`, pas dans
la variable). La « récurrence » qu'on croyait lire n'existe pas : c'est un simple décalage
dépendant de la position. C'est ce qui bloquait la session précédente (15 variantes testées,
toutes fausses, alors que la bonne hypothèse était *aucune récurrence*).

## Anti-debug = compteur de mutations

Sept sites d'appel à `mutate`, avec `n = 3, 2, 2, 1, 1, 2` puis `1` : **chaque détection de
débogueur ajoute une corruption de la clé**. `DetectDebuggerAtLaunch` (`0x402d00`) boucle
(`Sleep(0x1388)`, 0x40d0ec…) et ne laisse arriver à `0x4038e0` que si rien n'est détecté.

Sur un run propre, le total est `3+2+2+1+1+2+1 = 12`. Chaque passe ajoute `pc_j` mod 26, donc
la clé est **périodique de 26 en N** : `N ≡ 12 (mod 26)` → `academy{…}` (N=168 donne le même
résultat, d'où la régularité observée dans le balayage).

## Méthode retenue : Unicorn, pas de Wine

`wine32` impossible à installer (i386 à 100 Ko/s). Inutile : `mutate` et `DecryptFlag` ne
dépendent que de `config.bin`. On mappe le PE dépacké à `0x400000`, on écrit les trois globales,
on pousse l'argument et on `emu_start` sur les deux fonctions :

```
$ python3 _z_430_emu.py u300.exe config.bin 402bc0 402cb0 40c3d8 40c3d0 40c3d4
letters avant : wgzbvfboktzkztyhzinqrvnfnzkrnukmerdgomoj
cle muee      : ...
FLAG          : academy{Wind0ws_antid3bg_0x300_f57a6e29}
```

Le même émulateur valide `0x200` (même code, autres adresses de globales).

## Scripts

- `D:\ctf-index\_z_430_emu.py` — émulateur Unicorn PE32 (mutate + DecryptFlag).
- `D:\ctf-index\_z_430_scanN.py` — balayage de N pour les deux `config.bin`.
- `D:\ctf-index\_z_430_key.py` — dérivation de la clé attendue depuis le préfixe `academy{`.
