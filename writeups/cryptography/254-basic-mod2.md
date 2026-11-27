# basic-mod2

**Catégorie** : Cryptography · **Challenge** : #254 · **Résolu le** : 2026-11-23

## Énoncé

> A new modular challenge!
> Download the message [here](https://challenge-files.cylabacademy.net/library/8493f8b1c07d84e858fa52d3dacdc63752275286da7a30b69fab36993eafb5ea/message.txt).
>
> Take each number mod 41 and find the modular inverse for the result. Then map
> to the following character set: 1-26 are the alphabet, 27-36 are the decimal
> digits, and 37 is an underscore.
>
> Wrap your decrypted message in the academy flag format
> (i.e. `academy{decrypted_message}`)

## Résolution

Méthode : **mod 41 + inverse modulaire**.

Chaque nombre mod 41, puis on prend l'**inverse modulaire** (`pow(r,-1,41)`), puis mapping : 1-26 -> A-Z, 27-36 -> chiffres, 37 -> `_`. L'inverse est l'étape que tout le monde oublie.

## Flag

```
academy{1NV3R53LY_H4RD_950D690F}
```
