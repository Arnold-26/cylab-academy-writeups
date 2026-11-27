# CanYouSee

**Catégorie** : Forensics · **Challenge** : #408

## Énoncé

> How about some hide and seek?
>
> Download this file [here](https://challenge-files.cylabacademy.net/library/26d33b97d1745fc99c1cf94e3783a3dc963b8b667ca6960ebfce48aa9909251c/unknown.zip).

## Résolution

`exiftool` : le champ XMP **Attribution URL** contient du base64 → décodé.

## Flag

```
academy{ME74D47A_HIDD3N_aebe8c0f}
```

## Ce qu'il faut retenir

XMP est aussi un champ de métadonnées, pas seulement EXIF.
