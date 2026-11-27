# basic-mod1

**Catégorie** : Cryptography · **Challenge** : #253 · **Résolu le** : 2026-11-23

## Énoncé

> We found this weird message being passed around on the servers, we think we
> have a working decryption scheme.
> Download the message [here](https://challenge-files.cylabacademy.net/library/23b095a85da350dcda44aefdf5a62785a023f5d4570374d08eef71aefd096f7f/message.txt).
>
> Take each number mod 37 and map it to the following character set: 0-25 is the
> alphabet (uppercase), 26-35 are the decimal digits, and 36 is an underscore.
>
> Wrap your decrypted message in the academy flag format
> (i.e. `academy{decrypted_message}`)

## Résolution

Méthode : **mod 37 + charset**.

Chaque nombre modulo 37 : 0-25 -> A-Z, 26-35 -> chiffres, 36 -> `_`. Concaténer puis envelopper dans le format du flag.

## Flag

```
academy{R0UND_N_R0UND_81CE8A51}
```
