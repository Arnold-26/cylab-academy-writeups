# Invisible WORDs

**Catégorie** : Forensics · **Challenge** : #354 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **ZIP cache dans un BMP (2 octets sur 4)**.

Le BMP 960x540 32bpp contient un **ZIP** a l'offset 0x8c, mais chaque groupe de 4 octets n'en garde que 2 (les 2 autres sont du remplissage). On lit `data[i:i+2]` en sautant de 4 en 4 depuis 0x8c jusqu'a tomber sur `\xff\x00`, on ecrit le ZIP, on l'ouvre : il contient `ZnJhbmtlbnN0ZWluLXRlc3QudHh0` (= base64 de `frankenstein-test.txt`, le texte de Frankenstein) qui contient le flag.

## Flag

```
academy{w0rd_d4wg_y0u_f0und_5h3113ys_m4573rp13c3_2a058da1}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_354a.py`](../../solve/354/_z_354a.py)
- [`_z_354b.py`](../../solve/354/_z_354b.py)
- [`_z_354c.py`](../../solve/354/_z_354c.py)
- [`_z_354d.py`](../../solve/354/_z_354d.py)
- [`_z_354e.py`](../../solve/354/_z_354e.py)
- [`_z_354f.py`](../../solve/354/_z_354f.py)
- [`_z_354g.py`](../../solve/354/_z_354g.py)
- [`_z_354h.py`](../../solve/354/_z_354h.py)
- [`_z_354i.py`](../../solve/354/_z_354i.py)
- [`_z_354j.py`](../../solve/354/_z_354j.py)
- [`_z_354k.py`](../../solve/354/_z_354k.py)
