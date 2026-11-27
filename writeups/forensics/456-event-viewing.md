# Event-Viewing

**Catégorie** : Forensics · **Challenge** : #456 · **Résolu le** : 2026-11-24

## Énoncé

> One of the employees at your company has their computer infected by malware! Turns out every time they try to switch on the computer, it shuts down right after they log in. The story given by the employee is as follows:
>
> 1. They installed software using an installer they downloaded online
> 2. They ran the installed software but it seemed to do nothing
> 3. Now every time they bootup and login to their computer, a black command prompt screen quickly opens and closes and their computer shuts down instantly.
>
> See if you can find evidence for the each of these events and retrieve the flag (split into 3 pieces) from the correct logs!
>
> Download the Windows Log file [here](https://challenge-files.cylabacademy.net/library/ce601bcb71ad064088b71881564ee20ccdc62d9ec1dc7519d06b758a2e1f1efa/Windows_Logs.evtx)

## Résolution

Méthode : **evtx : fragments base64 dans 3 evenements**.

Le log contient l'installation de `Totally_Legit_Software.msi` (1033/1040), une modification de registre (4657) pointant vers `custom_shutdown.exe`, et un arret force (1074) dont le champ `param6` contient la fin du flag en base64 (`dDAwbF84MWJhM2ZlOX0=` -> `t00l_81ba3fe9}`).

## Flag

```
academy{Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9}
```

## Scripts

- [`solve.py`](../../solve/456/solve.py)
