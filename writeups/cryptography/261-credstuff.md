# credstuff

**Catégorie** : Cryptography · **Challenge** : #261 · **Résolu le** : 2026-11-23

## Énoncé

> We found a leak of a blackmarket website's login credentials. Can you find the
> password of the user `cultiris` and successfully decrypt it?
> Download the leak [here](https://challenge-files.cylabacademy.net/library/7f760cee144ac7237469fd6bfab7c748d6f1d101ca47c101187ca7d8f5c721f0/leak.tar).
>
> The first user in `usernames.txt` corresponds to the first password in
> `passwords.txt`. The second user corresponds to the second password, and so on.

## Résolution

Méthode : **index parallele + ROT13**.

`leak.tar` contient `usernames.txt` et `passwords.txt` (505 lignes chacun, listes paralleles). On cherche `cultiris` à l'index i et on prend le mot de passe au même index : `npnqrzl{P7e1S_54I35_71Z3}`, qui est du **ROT13** -> `academy{C7r1F_54V35_71M3}`.

## Flag

```
academy{C7r1F_54V35_71M3}
```
