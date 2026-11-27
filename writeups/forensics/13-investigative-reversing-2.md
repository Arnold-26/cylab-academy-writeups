# Investigative Reversing 2

**Catégorie** : Forensics · **Challenge** : #13 · **Résolu le** : 2026-11-25

## Énoncé

> A binary and an encoded BMP.

## Résolution

Méthode : **lsb stego**.

Le binaire copie les **2000 premiers octets** (`0x7d0`) du BMP, puis encode le flag,
puis recopie le reste. L'encodage est un **LSB par octet** via `codedChar` :

```c
char codedChar(int idx, char value, char pixel) {
    if (idx) value >>= idx;      // bit idx du caractere
    value &= 1;
    pixel &= 0xfe;
    return pixel | value;        // LSB du pixel = bit idx du caractere
}
```

8 octets par caractere, `j = 0..7`, et le caractere stocke est `flag[i] - 5`.
Decodage :

```python
for i in range(len(flag)):
    v = 0
    for j in range(8):
        v |= (bmp[2000 + i*8 + j] & 1) << j
    flag += chr((5 + v) & 0xff)
```

Resultat : `academy{n3xt_0n30000000000000000000000000c4bf77ad}` (50 caracteres).
Les octets au-dela du `}` sont du bruit de pile (le buffer de 50 octets n'est pas
initialise) : couper au premier `}`.

## Flag

```
academy{n3xt_0n30000000000000000000000000c4bf77ad}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_13a.sh`](../../solve/13/_z_13a.sh)
- [`_z_13b.sh`](../../solve/13/_z_13b.sh)
- [`_z_13c.sh`](../../solve/13/_z_13c.sh)
- [`_z_13d.py`](../../solve/13/_z_13d.py)
- [`_z_13e.py`](../../solve/13/_z_13e.py)
- [`_z_13f.sh`](../../solve/13/_z_13f.sh)
- [`_z_13g.py`](../../solve/13/_z_13g.py)
- [`_z_13h.py`](../../solve/13/_z_13h.py)
- [`_z_13i.py`](../../solve/13/_z_13i.py)
- [`_z_13j.sh`](../../solve/13/_z_13j.sh)
