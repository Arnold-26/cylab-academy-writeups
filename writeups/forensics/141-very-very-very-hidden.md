# Very very very Hidden

**Catégorie** : Forensics · **Challenge** : #141 · **Résolu le** : 2026-11-25

## Énoncé

> try_me.pcap (9,7 Mo)

## Résolution

Méthode : **Invoke-PSImage : script PowerShell dans les 4 bits de poids faible, puis XOR**.

Le pcap contient du TLS et du HTTP en clair ; `tshark --export-objects http` en extrait `duck.png`, `evil_duck.png`, `favicon.ico` et `NothingSus`. Les deux images font exactement 1223x812 mais `evil_duck.png` pese presque le double (2,5 Mo contre 1,3 Mo) : c'est le signal d'un **payload embarque** (Invoke-PSImage), pas d'une difference visuelle — la soustraction des deux images ne montre que le fantome de la photo et `steghide`/`zsteg` echouent tous deux. Le format Invoke-PSImage stocke **4 bits par pixel** : nibble haut dans le canal BLEU, nibble bas dans le canal VERT, ce qui se lit par `((B & 0xF) << 4) | (G & 0xF)` ligne par ligne. On obtient un script PowerShell de 396 octets qui declare deux chaines et fait `$bytes[$i] -bxor $data1[$i]` avant d'ecrire `flag.txt`. Le XOR octet a octet des deux chaines (49 caracteres chacune) donne directement le drapeau. Verification utile : l'ordre GB donne du bruit, seul BG fonctionne ; et `zsteg` echoue car il ne teste qu'un bit par canal alors qu'ici c'est un nibble.

## Flag

```
academy{n1c3_job_f1nd1ng_th3_s3cr3t_in_the_im@g3}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_141a.sh`](../../solve/141/_z_141a.sh)
- [`_z_141b.sh`](../../solve/141/_z_141b.sh)
- [`_z_141c.py`](../../solve/141/_z_141c.py)
- [`_z_141c.sh`](../../solve/141/_z_141c.sh)
- [`_z_141d.py`](../../solve/141/_z_141d.py)
- [`_z_141e.py`](../../solve/141/_z_141e.py)
- [`_z_141f.py`](../../solve/141/_z_141f.py)
- [`_z_141g.py`](../../solve/141/_z_141g.py)
- [`_z_141h.py`](../../solve/141/_z_141h.py)
- [`_z_141i.py`](../../solve/141/_z_141i.py)
- [`_z_141j.py`](../../solve/141/_z_141j.py)
- [`_z_141k.py`](../../solve/141/_z_141k.py)
