# droids3

**Catégorie** : Reverse Engineering · **Challenge** : #23 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **deobfuscation native : XOR répétitif dans sumac()**.

APK decompile avec apktool ; `FlagstaffHill.cilantro(String)` est natif et renvoie `sumac()` (le flag) si `dill(input)` est vrai. `sumac` fait `unscramble(str2, 26, strdup(str1), strlen(str1))` ou `unscramble` est un **XOR repetitif** : `out[i] ^= key[i % keylen]`. Cle a 0x1a0d = `againmissing`, donnees a 0x1a85 (26 octets) -> `academy{tis.but.a.scratch}`. Le mot de passe attendu cote app est `don't wanna`. La lib est compilee pour Bionic (exige la version symbole `LIBC`), donc le `dlopen` sous glibc echoue : il faut decoder statiquement (neutraliser `.gnu.version`/`vn_cnt` ne suffit pas).

## Flag

```
academy{tis.but.a.scratch}
```

## Ce qu'il faut retenir

—
