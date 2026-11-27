# Rust fixme 1

**Catégorie** : Général Skills · **Challenge** : #461 · **Résolu le** : 2026-11-23

## Énoncé

> Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag!
>
> Download the Rust code [here](https://challenge-files.cylabacademy.net/library/b9cfc84c442958b8ac848ddc0692bed9ef01a15877b8d37f36afbe68b5849acc/fixme1.tar.gz).

## Résolution

Méthode : **correction Rust + compilation**.

Le source Rust est cassé expres. Corrections : `;` manquant, `ret` -> `return`, `println!(":?")` -> `println!("{:?}", ...)`, `&String` -> `&mut String` avec `let mut`, decommenter `unsafe`. Compilation via `PATH=/usr/bin:/bin RUSTC=/usr/bin/rustc cargo run` (le shim rustup casse sinon).

## Flag

```
academy{4r3_y0u_4_ru$t4c30n_n0w?}
```
