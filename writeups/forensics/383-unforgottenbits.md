# UnforgottenBits

**Catégorie** : Forensics · **Challenge** : #383 · **Résolu le** : 2026-11-25

## Énoncé

> disk.flag.img (1 Go) + 4 BMP de la galerie

## Résolution

Méthode : **steghide (mot de passe LoL) + AES-256-CBC avec sel/cle/IV specifiques**.

Image disque de 1 Go (`disk.flag.img`) a analyser. Le writeup donne la chaine complete, que j'ai reexecutee pas a pas. Etape 1 : extraire les 4 images de la galerie (`home/yone/gallery/{1,2,3,7}.bmp`) avec `fls`/`icat` de sleuthkit. Etape 2 : un log IRC (`irclogs/01/04/#avidreader13.log`) revele la methode — **steghide** avec le mot de passe `akalibardzyratrundle`, puis **AES-256-CBC**. Les images 1, 2 et 3 se decodent bien et donnent des ebooks Gutenberg (Les Miserables, Dracula, Frankenstein) : ce sont des leurres, `grep` n'y trouve aucun flag. L'image **7.bmp** refuse ce mot de passe. Etape 3 : le writeup explique que le mot de passe de 7.bmp est compose de **champions de League of Legends** (indice : les notes `1.txt`/`2.txt`/`3.txt` contiennent `chizazerite`, `guldulheen`, et surtout `yasuoaatrox...`), a casser avec `stegcracker`. Le mot de passe est **`yasuoaatroxashecassiopeia`**. Etape 4 : les 560 octets extraits se dechiffrent avec `openssl enc -aes-256-cbc -d -S 2350e88cbeaf16c9 -K a9f86b...36da -iv 908458e4...119f` (sel, cle et IV differents de ceux des trois autres images, encore un piege) et donnent une liste de clients ressemblant a une bibliotheque, avec la ligne `academy{f473_53413d_e0c91991}`. Lecons : (1) plusieurs jeux de parametres de chiffrement cohabitent, il faut traiter chaque image separement ; (2) trois des quatre images sont des leurres plausibles ; (3) le vrai secret passe par un mot de passe thematique a casser, pas par une analyse forensique directe.

## Flag

```
academy{f473_53413d_e0c91991}
```

## Ce qu'il faut retenir

steghide exige une passphrase : elle est souvent dans les metadonnees.

## Scripts

- [`_z_383a.py`](../../solve/383/_z_383a.py)
- [`_z_383a.sh`](../../solve/383/_z_383a.sh)
- [`_z_383b.sh`](../../solve/383/_z_383b.sh)
- [`_z_383c.sh`](../../solve/383/_z_383c.sh)
- [`_z_383d.sh`](../../solve/383/_z_383d.sh)
- [`_z_383e.py`](../../solve/383/_z_383e.py)
- [`_z_383e.sh`](../../solve/383/_z_383e.sh)
- [`_z_383f.py`](../../solve/383/_z_383f.py)
- [`_z_383f.sh`](../../solve/383/_z_383f.sh)
- [`_z_383g.py`](../../solve/383/_z_383g.py)
- [`_z_383g.sh`](../../solve/383/_z_383g.sh)
- [`_z_383h.sh`](../../solve/383/_z_383h.sh)
- [`_z_383i.py`](../../solve/383/_z_383i.py)
- [`_z_383i.sh`](../../solve/383/_z_383i.sh)
- [`_z_383j.sh`](../../solve/383/_z_383j.sh)
- [`_z_383k.py`](../../solve/383/_z_383k.py)
- [`_z_383l.sh`](../../solve/383/_z_383l.sh)
- [`_z_383m.py`](../../solve/383/_z_383m.py)
- [`_z_383n.py`](../../solve/383/_z_383n.py)
- [`_z_383o.py`](../../solve/383/_z_383o.py)
