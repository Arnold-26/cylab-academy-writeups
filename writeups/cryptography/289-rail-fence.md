# rail-fence

**Catégorie** : Cryptography · **Challenge** : #289 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **rail fence 4 rails**.

Transposition rail fence a 4 rails. On reconstruit le motif en zigzag (0,1,2,3,2,1,0,...), on repartit le texte chiffre par lignes selon le nombre de caracteres de chaque rail, puis on relit dans l'ordre du motif.

## Flag

```
academy{WH3R3_D035_7H3_F3NC3_8361N_4ND_3ND_43BBCEC4}
```
