# Rust fixme 2

**Catégorie** : Général Skills · **Challenge** : #462 · **Résolu le** : 2026-11-23

## Énoncé

> The Rust saga continues? I ask you, can I borrow that, pleeeeeaaaasseeeee?
>
> Download the Rust code [here](https://challenge-files.cylabacademy.net/library/048c73621a97b98cde18eae5a9495279f2396cb64c65235bb310e7ad26d726ac/fixme2.tar.gz).

## Résolution

Méthode : **correction Rust + compilation**.

Le source Rust est cassé expres. Corrections : `;` manquant, `ret` -> `return`, `println!(":?")` -> `println!("{:?}", ...)`, `&String` -> `&mut String` avec `let mut`, decommenter `unsafe`. Compilation via `PATH=/usr/bin:/bin RUSTC=/usr/bin/rustc cargo run` (le shim rustup casse sinon).

## Flag

```
academy{4r3_y0u_h4v1n5_fun_y31?}
```
