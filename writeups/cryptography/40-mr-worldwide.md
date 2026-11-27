# Mr-Worldwide

**Catégorie** : Cryptography · **Challenge** : #40 · **Résolu le** : 2026-11-23

## Énoncé

> A musician left us a [message](https://challenge-files.cylabacademy.net/library/1c5f1bab1a3c5a977353b740cb58a88381e3a9fd0ea26b4a3a1bfe5c2ffdb021/message.txt). What's it mean?

## Résolution

Méthode : **geolocalisation -> initiales**.

Le fichier contient 12 paires de coordonnées. Chacune correspond à une ville ; l'initiale de la ville donne une lettre. Sequence : Kyoto, Odesa, Dayton, Istanbul, Abu Dhabi, Kuala Lumpur, Addis Ababa, Loja, Amsterdam, Stamford, Kodiak, Alexandria -> `KODIAK_ALASKA`.

## Flag

```
academy{KODIAK_ALASKA}
```
