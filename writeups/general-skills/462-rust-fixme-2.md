# Rust fixme 2

**Catégorie** : General Skills · **Challenge** : #462 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **correction Rust + compilation**.

Le source Rust est casse expres. Corrections : `;` manquant, `ret` -> `return`, `println!(":?")` -> `println!("{:?}", ...)`, `&String` -> `&mut String` avec `let mut`, decommenter `unsafe`. Compilation via `PATH=/usr/bin:/bin RUSTC=/usr/bin/rustc cargo run` (le shim rustup casse sinon).

## Flag

```
academy{4r3_y0u_h4v1n5_fun_y31?}
```

## Ce qu'il faut retenir

—
