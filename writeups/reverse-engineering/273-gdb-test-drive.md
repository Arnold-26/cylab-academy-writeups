# GDB Test Drive

**Catégorie** : Reverse Engineering · **Challenge** : #273 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get the flag?
> Download this [binary](https://challenge-files.cylabacademy.net/library/37a3037cc617e25371d3529e74304830bd22988c8c2f2b39e4355fc6781ac402/gdbme).
>
> Here's the test drive instructions:
> - `$ chmod +x gdbme`
> - `$ gdb gdbme`
> - `(gdb) layout asm`
> - `(gdb) break *(main+99)`
> - `(gdb) run`
> - `(gdb) jump *(main+104)`

## Résolution

Méthode : **saut par-dessus le sleep**.

Le binaire fait un `sleep` avant d'afficher le flag. On casse à `main+99`, on lance, puis `jump *(main+104)` saute le sleep ; `continue` affiche le flag.

## Flag

```
academy{d3bugg3r_dr1v3_d28daa02}
```
