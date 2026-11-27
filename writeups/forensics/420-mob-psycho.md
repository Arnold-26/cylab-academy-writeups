# Mob psycho

**Catégorie** : Forensics · **Challenge** : #420 · **Résolu le** : 2026-11-23

## Énoncé

> Can you handle APKs?
>
> Download the android apk [here](https://challenge-files.cylabacademy.net/library/1a512a3cd1665abd303e0ce89b954eb939e750f97b7e6ec2f176efddebbe9e86/mobpsycho.apk).

## Résolution

Méthode : **unzip APK + hex**.

L'APK contient `res/color/flag.txt` dont le contenu est une chaîne **hexadécimale**. Un simple `bytes.fromhex()` donne le flag.

## Flag

```
academy{ax8mC0RU6ve_NX85l4ax8mCl_2196cbb9}
```
