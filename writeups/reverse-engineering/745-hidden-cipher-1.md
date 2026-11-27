# 745 — Hidden Cipher 1

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

> The flag is right in front of you, just slightly encrypted. Figure out the cipher and the key. Download the binary and the encoded flag.

L'archive `hiddencipher.zip` contient le binaire et le fichier de flag encodé.

## Analyse

### Premier regard sur le binaire

```bash
file hiddencipher
# ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Packed with UPX
```

La mention `Packed with UPX` est déjà la réponse à l'indice du challenge : « a tool often pre-installed on Linux » désigne UPX, le packer d'exécutables le plus courant sur les distributions. Le binaire n'a pas de symboles exploitables tant qu'il est compressé.

### Après décompression

Une fois décompressé et chargé dans Ghidra, `main()` redevient lisible. La structure est simple :

1. lecture du fichier de flag encodé, en externe, via `fread` ;
2. appel de `get_secret()` pour récupérer la clé ;
3. boucle de déchiffrement sur chaque octet ;
4. affichage ou comparaison du résultat.

La boucle est un XOR indexé :

```c
for (i = 0; i < len; i++)
    out[i] = enc[i] ^ key[i % 6];
```

La clé est de **6 octets** et se trouve dans la fonction voisine `get_secret()`, sous une forme légèrement obfusquée : les octets ne sont pas écrits en clair dans une chaîne littérale, ils sont assemblés par quelques opérations avant d'être retournés. C'est ce qui fait la différence entre « lire le flag dans `strings` » et « comprendre le déchiffrement ».

Le point clé de l'analyse : le XOR est sa propre inverse. `a ^ k ^ k = a`. Il n'y a donc pas d'algorithme de déchiffrement distinct à reconstruire : la même opération, avec la même clé, appliquée au chiffré, redonne le clair. Clé et chiffré suffisent.

## Solution

### 1. Décompresser le binaire

```bash
unzip hiddencipher.zip
sudo apt-get install -y upx-ucl
upx -d hiddencipher
file hiddencipher        # ELF 64-bit ... not stripped
```

Si `upx -d` refuse, on force la décompression :

```bash
upx -d -f hiddencipher
upx -t hiddencipher      # vérifie l'intégrité après coup
```

### 2. Localiser la boucle et la clé dans Ghidra

On ouvre le binaire, on accepte l'analyse automatique, puis on cherche `main` dans la liste des fonctions. On repère la boucle par deux indices : l'opérateur `^` et le modulo sur la longueur de clé (`% 6`). Le double-clic sur `get_secret` mène aux six octets.

Si l'obfuscation gêne la lecture statique, deux raccourcis :

```bash
gdb -q ./hiddencipher
(gdb) break get_secret
(gdb) run
(gdb) finish
(gdb) x/6xb $rax
```

En posant un point d'arrêt sur le retour de `get_secret()`, la clé est en mémoire, déjà reconstituée : l'obfuscation ne sert plus à rien.

### 3. Déchiffrer le fichier

```python
key = bytes.fromhex("a1b2c3d4e5f6")     # les 6 octets lus dans get_secret()
ct  = open("encrypted_flag", "rb").read()
pt  = bytes(c ^ key[i % len(key)] for i, c in enumerate(ct))
print(pt.decode(errors="replace"))
```

Même chose dans CyberChef : `From Hex` si le fichier est un texte hexadécimal, puis `XOR` avec la clé saisie en hexadécimal et le motif `Standard` (répétition de la clé).

### 4. Vérifier

Le clair doit commencer par `picoCTF{` et se terminer par `}`. Un résultat illisible signale une erreur sur la clé ou sur la longueur du motif.

### Pourquoi ça marche

Le XOR avec une clé courte répétée est un chiffrement de flux élémentaire : chaque octet de clair est transformé indépendamment, et l'opération est involutive. Il n'y a donc aucune clé à casser par force brute — six octets se liraient de toute façon instantanément — mais surtout aucune barrière cryptographique : la sécurité reposait entièrement sur le fait de cacher l'algorithme et la clé dans un binaire packé. La décompression et la décompilation rendent les deux visibles.

## Pièges

- **Lancer le binaire packé.** Un UPX non décompressé s'exécute normalement mais son code réel n'est visible qu'en mémoire : `strings` ne montre que le stub et rien d'utile.
- **Confondre longueur et période.** La clé fait 6 octets, mais le motif se répète sur toute la longueur : utiliser `i % 6` et non une clé étendue à la main.
- **Le fichier de flag en hexadécimal.** Si le fichier commence par des caractères `0-9a-f`, il faut d'abord le décoder (`bytes.fromhex`) avant d'appliquer le XOR, sinon on XOR des codes ASCII de chiffres hexadécimaux.
- **Un octet de trop.** Un `\n` final dans le fichier chiffré produit un caractère parasite en fin de clair ; ce n'est pas une erreur de clé.
- **Le mauvais endianness dans Ghidra.** Les six octets peuvent apparaître sous forme d'un entier 64 bits ; on relit octet par octet (`x/6xb` en GDB) plutôt que de recopier la valeur d'un `mov` en bloc.

## Flag

Flag validé sur la plateforme (valeur non conservée).
