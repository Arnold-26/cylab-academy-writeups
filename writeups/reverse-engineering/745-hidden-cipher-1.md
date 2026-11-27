# 745 — Hidden Cipher 1

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> The flag is right in front of you, just slightly encrypted. Figure out the cipher and the key.
> Download the binary and the encoded flag.

L'archive `hiddencipher.zip` contient le binaire et le fichier de flag encodé.

## Analyse

`file` identifie un ELF 64 bits **packé avec UPX** ; l'indice du challenge (« a tool often
pre-installed on Linux ») désigne justement UPX, à décompresser avec `upx -d`. Une fois le binaire
décompressé et chargé dans Ghidra, `main()` contient une boucle qui XOR chaque octet du flag avec
une clé de **6 octets** indexée modulo la longueur (`flag[i] ^ key[i % 6]`), la clé étant fournie
par la fonction voisine `get_secret()` sous forme légèrement obfusquée. Les octets du flag encodé
sont lus dans un fichier externe (`fread`). XOR étant sa propre inverse, la clé et le chiffré
suffisent.

## Solution

1. Décompresser le binaire :

```bash
unzip hiddencipher.zip
sudo apt-get install upx-ucl
upx -d hiddencipher
file hiddencipher     # ELF 64-bit ... not stripped
```

2. Dans Ghidra, ouvrir `main()` : repérer la boucle XOR et le modulo 6, puis naviguer vers
   `get_secret()` pour lire les 6 octets de clé.
3. Déchiffrer le fichier de flag avec CyberChef (`From Hex` puis `XOR` avec la clé) ou en Python :

```python
key = bytes.fromhex("<6 octets lus dans get_secret()>")
ct  = open("encrypted_flag", "rb").read()
print(bytes(c ^ key[i % len(key)] for i, c in enumerate(ct)).decode())
```

## Flag

```
picoCTF{xor_unpack_4nalys1s_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — Hidden Cipher 1 (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-hidden-cipher-1)
- [snwau/picoCTF-2026-Writeup — Reverse Engineering/Hidden Cipher 1](https://github.com/snwau/picoCTF-2026-Writeup/blob/main/Reverse%20Engineering/Hidden%20Cipher%201/Hidden%20Cipher%201.md)
- [HawkSec — Hidden Cipher 1](https://hawksec.gitbook.io/pt/writeups/picoctf/reverse-engineering/hidden-cipher-1)
