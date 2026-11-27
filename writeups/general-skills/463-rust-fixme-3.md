# Rust fixme 3

**Catégorie** : Général Skills · **Challenge** : #463 · **Résolu le** : 2026-11-23

## Énoncé

> Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag!
>
> Download the Rust code [here](https://challenge-files.cylabacademy.net/library/6df8b7779faf29e53f515922041d99bc26381a332ca090c291ba20577ac7cf92/fixme3.tar.gz).

## Résolution

Méthode : **correction Rust + compilation**.

Le source Rust est cassé expres. Corrections selon le niveau : `;` manquant après `let key`, `ret` -> `return`, `println!(":?")` -> `println!("{:?}", ...)`, `&String` -> `&mut String` (avec `let mut`), et decommenter le bloc `unsafe` autour de `std::slice::from_raw_parts`. Puis `cargo run`.

## Flag

```
academy{n0w_y0uv3_f1x3d_1h3m_411}
```
