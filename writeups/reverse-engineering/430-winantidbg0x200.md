# 430 — WinAntiDbg0x200 — Reverse Engineering

**Flag :** `academy{0x200_debug_f0r_Win_0d811b88}`
**Artefacts :** `WinAntiDbg0x200.exe` (PE32, 16 384 o) + `config.bin` (80 o), zip protégé par
le mot de passe `academy`.

## Idée directe : pas de Windows, pas de wine32 → on exécute les vraies fonctions

Le binaire est un PE32 qui refuse de tourner sous un débogueur, et `wine32` n'était pas
installable (miroir i386 à ~100 Ko/s). Inutile d'ailleurs : **le flag ne dépend que de
`config.bin`**. On isole les deux fonctions qui le transforment et on les fait exécuter par
**Unicorn** (`UC_MODE_32`), en mappant l'image PE à son `ImageBase` et en appelant directement
`mutate` puis `DecryptFlag` — zéro dépendance à Windows, zéro devinette sur le désassemblage.

## `config.bin` — layout exact (déduit de `ReadConfig`)

```
[0x00] u32 size                       (40 pour 0x300, 37 pour 0x200)
[0x04] size octets  : lettres a-z      <- matériau de clé
[+size+1] size octets : flag XORé
taille totale du fichier = 4 + 2*size + 2
```

`ReadConfig` impose `n_lus > 0 && size < 200 && n_lus == 2*size + 2`, puis :

```c
CONFIG_BUFFER = malloc(0xc8);            // 0x40c3d0 (0x200 : autre adresse)
fread(&FLAG_SIZE, 1, 4, fp);             // 0x40c3d8 = size
fread(CONFIG_BUFFER, 1, 0xc8, fp);
for (i = 0; i < n; i++)
    if (i == FLAG_SIZE && FLAG == NULL)
        FLAG = CONFIG_BUFFER + i + 1;    // 0x40c3d4 = buffer + size + 1
```

## `mutate(n)` — le « chiffrement » de la clé

Désassemblé à `0x402bc0` (0x300) ; le code de 0x200 est identique. **Le piège** : `ch` est
initialisé à `0x61` (`[ebp-1]`) et **jamais réécrit** — ce n'est pas une récurrence, c'est un
décalage par position :

```c
for (k = 0; k < n; k++)
  for (j = 0; j < size; j++) {
      int m  = j % 255;
      int T  = (m & 0x55) + ((m >> 1) & 0x55);
      int U  = (T & 0x33) + ((T >> 2) & 0x33);
      int pc = (U & 0x0f) + ((U >> 4) & 0x0f);        // = popcount(j % 255)
      int v  = buf[j] - 'a' + pc;                     // movzx - movsx + pc
      buf[j] = 'a' + (v % 26);                        // idiv => modulo C signé
  }
```

`DecryptFlag(key)` (`0x402cb0`) : `FLAG[i] ^= key[i]` pour `i < size`.

Conséquence utile : chaque passe ajoute `pc_j` modulo 26 à l'octet `j`, donc
`key_j(N) = 'a' + ((L_j - 'a' + N*pc_j) % 26)` — **la clé est périodique de 26 en N**.

## L'anti-debug, c'est le compteur N

Il y a **7 sites d'appel** à `mutate` avec des `n` différents (3, 2, 2, 1, 1, 2, puis 1) : chaque
détection de débogueur en appelle un de plus et **corrompt la clé** (« the flag might get
corrupted if you mess up the process's state »). Sur un run propre, tous s'exécutent :
`3+2+2+1+1+2+1 = 12`.

```
N = 12 (mod 26) == 168 (mod 26) = 12   ->  même clé, même flag
```

## Résultat

```
$ python3 _z_430_emu.py u300.exe config.bin 402bc0 402cb0 40c3d8 40c3d0 40c3d4
cle muee : ...
academy{0x200_debug_f0r_Win_0d811b88}
```

Le balayage de `N` reste une solution de repli robuste (`_z_430_scanN.py` : N=0..1023, filtre
« 100 % ASCII imprimable ») — c'est elle qui a livré le flag, Unicorn servant à prouver que le
décodage de l'ASM était bon.

## Scripts

- [`solve.py`](../../solve/430/solve.py)
- *22 variantes intermediaires dans `solve/430/archive/`*
