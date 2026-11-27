# Flag Hunters

**Catégorie** : Reverse Engineering · **Challenge** : #472 · **Résolu le** : 2026-11-23

## Énoncé

> Lyrics jump from verses to the refrain kind of like a subroutine call. There's
> a hidden refrain this program doesn't print by default. Can you get it to print
> it? There might be something in it for you.
>
> The program's source code can be downloaded
> [here](https://challenge-files.cylabacademy.net/library/659de58d4def8163cd0116c565d8900a309427071dc758473385f9468d93370f/lyric-reader.py).

## Résolution

Méthode : **injection au prompt Crowd**.

Le lecteur de paroles remplace la ligne CROWD par `'Crowd: ' + input` puis la re-decode avec `split(';')`. En envoyant `;RETURN 0` (sans espace après le point-virgule), on injecte une commande `RETURN 0` qui remonte au debut du morceau, ou se trouve le flag.

## Flag

```
academy{70637h3r_f0r3v3r_697ad4d5}
```
