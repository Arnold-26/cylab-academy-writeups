# 318 — Wizardlike — Reverse Engineering

**Flag :** `academy{ur_4_w1z4rd_e14455ad}`
**Binaire :** `_z_game` — ELF x86-64 **statique non-PIE**, 1 203 016 o, **strippé**, sans instance
réseau (le flag est dérivé du binaire lui-même).

## Le flag est *dessiné*, pas stocké

Aucune chaîne `academy{` ni lettre dans le binaire : les cartes ne contiennent que `' '`, `'#'`,
`'.'`, `'<'`, `'>'`. Le flag n'est donc pas une donnée mais une **image** : chaque niveau a, sur son
sol, le fragment suivant du flag **rastérisé en glyphes `#`** avec une police bitmap 5×5
(les trous sont `.` ou `' '`).

## Cartographie (le vrai déblocage : une stride fausse de 80 octets)

- Les 11 cartes sont en `.data` : offset fichier `0x107100` = VMA **0x508100**.
- **Stride réel = 0x2720** (10 016 = 100×100 tuiles + 16 octets de zéro), et non 0x2770 comme
  estimé auparavant — ce décalage de 80 o par bloc faisait paraître le 11ᵉ bloc incohérent.
- `main` à `0x402053` : switch niveau 1..10 → `0x50a820, 0x50cf40, 0x50f660, 0x511d80, 0x5144a0,
  0x516bc0, 0x5192e0, 0x51ba00, 0x51e120, 0x520840`. La carte 0 (`0x508100`) n'est **jamais**
  référencée par le code.
- `0x401a6d` copie la carte du niveau dans un buffer de travail `0x5275a0` (c'est **lui** que lit la
  collision, pas le tableau `.data`) ; `0x401da4` = test de collision (`'#'`/`' '` bloquent) ;
  `0x401b0e` = ligne de vue ; `0x401a05`/`0x524e80` = bitmap de visibilité ; `0x4097c0` = `mvaddch`.
  Conclusion : **seuls les caractères de la carte et `@` sont dessinés** → pas de routine de
  décodage cachée.

## Lecture du flag, niveau par niveau

| Niveau | Fragment | Emplacement |
|---|---|---|
| 1 | `academy{` | rows 3-6, cols 12-51 (8 glyphes, cols 12/17/22/27/32/37/42/47) |
| 2 | `ur_4_w1z4rd_` | rows 1-4, cols 8-66 (12 glyphes, deux barres `_` au baseline) |
| 3 | `e` | 5×5 en r1-5 c21-25 |
| 4 | `1` | r1-5 c22-24 |
| 5 | `4` | r5 couche 2, c18-22 |
| 6 | `4` | r15-19 |
| 7 | `5` | — |
| 8 | `5` | glyphe identique à L7 |
| 9 | `a` | r1-5 c94-98 |
| 10 | `d}` | r34-38 c86-90 + c92-94 |

`academy{` + `ur_4_w1z4rd_` + `e` + `1` + `4` + `4` + `5` + `5` + `a` + `d` + `}`

## Deux pièges

1. Dans la police 5×5, **`5` et `S` sont pixel-identiques** (`4`/`y` presque) : `e144ssad`,
   `E144SSAD` et `e14455ad` ont tous été essayés ; seul `...e14455ad` est accepté.
2. La forme en map 4 (rows 1-5, cols 13-16 : `####/...#/...#/...#/####`) est **l'encadrement de la
   porte `>`**, pas une lettre — la compter ajoute un `c` fantôme et casse le flag.

## Scripts

- [`_z_318a.sh`](../../solve/318/_z_318a.sh)
