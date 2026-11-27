# Operation Oni

**Catégorie** : Forensics · **Challenge** : #284 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **cle SSH dans l'image disque**.

Image a deux partitions. Dans la 2e (offset 206848), `/root/.ash_history` montre un `ssh-keygen` et `/root/.ssh/id_ed25519` (inode 2345) contient la cle privee. Il faut la copier hors de `/mnt/c` et `chmod 600` pour que ssh l'accepte.

## Flag

```
academy{k3y_5l3u7h_127b8b44}
```

## Ce qu'il faut retenir

—
