# rail-fence

**Catégorie** : Cryptography · **Challenge** : #289 · **Résolu le** : 2026-11-23

## Énoncé

> A type of transposition cipher is the rail fence cipher, which is described
> [here](https://en.wikipedia.org/wiki/Rail_fence_cipher). Here is one such
> cipher encrypted using the rail fence with 4 rails. Can you decrypt it?
> Download the message [here](https://challenge-files.cylabacademy.net/library/d6cea3d41550d2d3e365dd3a7ea99fe9b44fe5fa437d1c921b5134a2070894a5/message.txt).
>
> The decoded message names a phrase. Put that phrase, and nothing else, in the
> academy flag format: `academy{phrase}`.

## Résolution

Méthode : **rail fence 4 rails**.

Transposition rail fence a 4 rails. On reconstruit le motif en zigzag (0,1,2,3,2,1,0,...), on repartit le texte chiffre par lignes selon le nombre de caractères de chaque rail, puis on relit dans l'ordre du motif.

## Flag

```
academy{WH3R3_D035_7H3_F3NC3_8361N_4ND_3ND_43BBCEC4}
```
