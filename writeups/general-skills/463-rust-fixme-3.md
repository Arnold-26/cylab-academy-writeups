# Rust fixme 3

**Catégorie** : General Skills · **Challenge** : #463 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **correction Rust + compilation**.

Le source Rust est casse expres. Corrections selon le niveau : `;` manquant apres `let key`, `ret` -> `return`, `println!(":?")` -> `println!("{:?}", ...)`, `&String` -> `&mut String` (avec `let mut`), et decommenter le bloc `unsafe` autour de `std::slice::from_raw_parts`. Puis `cargo run`.

## Flag

```
academy{n0w_y0uv3_f1x3d_1h3m_411}
```

## Ce qu'il faut retenir

—
