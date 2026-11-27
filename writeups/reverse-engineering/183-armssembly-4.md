# ARMssembly 4

**Catégorie** : Reverse Engineering · **Challenge** : #183 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **interpretation a la main d'un .S ARM**.

Le source ARM64 `chall_4.S` : `main` appelle `func1(atoi(argv[1]))` avec a=965270072. `func1` : si a>100 -> `func2(a+100)` sinon `func3(a)`. `func2` : si x>499 -> `func5(x+13)` sinon `func4(x-86)`. `func5` -> `func8(x)` qui fait `x+2`. Chaine : 965270072 -> 965270172 -> 965270185 -> 965270187 = 0x39885dab. Les autres branches (`func3`/`func4`/`func6`/`func7`) ne sont jamais prises avec cette entree.

## Flag

```
academy{3988daab}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/183/solve.py)
