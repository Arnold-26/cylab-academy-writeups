# ARMssembly 4

**Catégorie** : Reverse Engineering · **Challenge** : #183 · **Résolu le** : 2026-11-24

## Énoncé

> What integer does this program print?
>
> Flag format: academy{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be academy{0055aabb})
> Use argument a: 965270072
>
> File: [chall_4.S](https://challenge-files.cylabacademy.net/library/2cbe7696e34dc7289d3f5843182804ee684517ee7d29cfa354c057a742b2cfcf/chall_4.S)

## Résolution

Méthode : **interpretation à la main d'un .S ARM**.

Le source ARM64 `chall_4.S` : `main` appelle `func1(atoi(argv[1]))` avec a=965270072. `func1` : si a>100 -> `func2(a+100)` sinon `func3(a)`. `func2` : si x>499 -> `func5(x+13)` sinon `func4(x-86)`. `func5` -> `func8(x)` qui fait `x+2`. Chaîne : 965270072 -> 965270172 -> 965270185 -> 965270187 = 0x39885dab. Les autres branches (`func3`/`func4`/`func6`/`func7`) ne sont jamais prises avec cette entrée.

## Flag

```
academy{3988daab}
```

## Scripts

- [`solve.py`](../../solve/183/solve.py)
