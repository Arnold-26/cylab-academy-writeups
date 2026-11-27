# Pico Bank

**Catégorie** : Reverse Engineering · **Challenge** : #529 · **Résolu le** : 2026-11-25

## Énoncé

> Audit de l'application mobile Pico Bank ; les identifiants d'un utilisateur ont fuite.

## Résolution

Méthode : **android apk reversing**.

Le site de l'instance sert un APK (`/download/pico-bank.apk`) et une API
(`POST /verify-otp`).

### 1. Decompiler l'APK

`apktool d` (ou `jadx`) donne les classes `Login`, `OTP`, `MainActivity`, `Transaction`.
Les ressources contiennent deja un secret :

```xml
<string name="otp_value">9673</string>
```

### 2. Le flag est coupe en deux

`POST /verify-otp` avec `{"otp": "9673"}` repond :

```json
{"success":true, "message":"OTP verified successfully",
 "flag":"s3cur3d_m0b1l3_l0g1n_7f1dd571}",
 "hint":"The other part of the flag is hidden in the app"}
```

La seconde moitie vient du serveur ; la premiere est dans l'app.

### 3. Decoder les montants binaires

`MainActivity` construit 26 `Transaction(description, date, montant, bool)`. Les montants sont
des **nombres binaires** :

```
$ 1100001 -> 97  -> a
$ 1100011 -> 99  -> c
...
$ 1111011 -> 123 -> {
$ 1011111 -> 95  -> _
```

Piege : le compilateur DEX **reutilise les registres**. Certaines transactions n'ont pas de
`const-string` de montant juste avant, elles referencent un registre encore rempli plus haut
(`v9`, `v10`, `v11`, `v12`). Il faut donc simuler l'affectation registre par registre en
parcourant le smali lineairement :

```python
reg = {}
for ln in lines:
    m = const-string (vN), "..."   -> reg[vN] = value
    m = invoke-direct {v4, vA, vB, vC, vD}, Transaction-><init>
        desc, date, amount = reg[vA], reg[vB], reg[vC]
```

En triant par date **decroissante** :

```
academy{1_l13d_4b0ut_b31ng_
```

On colle les deux moities :

```
academy{1_l13d_4b0ut_b31ng_s3cur3d_m0b1l3_l0g1n_7f1dd571}
```

### A retenir

- Un APK expose ses constantes : `strings.xml` pour l'OTP, smali pour les montants.
- Quand un `invoke` reference un registre sans `const-string` proche, c'est une **reutilisation
  de registre** : il faut tracer le flux, pas seulement grepper les chaines.
- Ici la difficulte n'etait pas l'endpoint (`/verify-otp` est evident) mais l'**ordre** des
  transactions : trier par date decroissante donne un texte lisible, l'ordre du fichier smali
  ne suffit pas.

## Flag

```
academy{1_l13d_4b0ut_b31ng_s3cur3d_m0b1l3_l0g1n_7f1dd571}
```

## Ce qu'il faut retenir

—
