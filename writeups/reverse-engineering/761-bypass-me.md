# 761 — Bypass Me

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

> Your task is to analyze and exploit a password-protected binary called `bypassme.bin`. The binary
> performs input sanitation. Instead of guessing the password, reverse engineer or debug the program
> to bypass the authentication logic and retrieve the hidden flag.

Le binaire est un exécutable **setuid** sur la machine distante, accessible en SSH avec le compte
fourni.

## Analyse

### Ce que fait le binaire

`main()` appelle `decode_password()` avant la séquence d'introduction. Cette fonction prend 12 octets
codés en dur et les XOR un par un avec la clé fixe `0xAA` pour produire le mot de passe attendu :

```c
char *decode_password(void) {
    unsigned char enc[12] = {0xD9,0xDF,0xDA,0xCF,0xD8,0x8A,
                             0xD9,0xCF,0xC9,0xDF,0xD8,0xCF};
    for (int i = 0; i < 12; i++) enc[i] ^= 0xAA;
    return (char *)enc;
}
```

C'est de l'obfuscation, pas du chiffrement : la clé est unique, constante, et visible dans le code.
Les 12 octets décodés donnent `super secure`.

### Deux voies équivalentes

1. **Statique** : décompiler avec Ghidra, relever les 12 octets, appliquer le XOR.
2. **Dynamique** : laisser le binaire décoder en mémoire et lire la valeur au moment de la
   comparaison, ce qui rend l'obfuscation inutile.

### Pourquoi l'exécution doit être distante

Le binaire est setuid : c'est lui qui porte les droits de lecture sur le fichier de flag. Une copie
locale n'a pas ces droits. On l'analyse en local, mais on l'exécute sur la machine distante.

## Solution

### 1. Récupérer le binaire

```bash
scp -P <PORT> ctf-player@<HOST>:bypassme.bin .
file bypassme.bin
checksec --file=bypassme.bin
```

### 2. Décoder le mot de passe

```bash
python3 - <<'EOF'
enc = bytes([0xD9,0xDF,0xDA,0xCF,0xD8,0x8A,0xD9,0xCF,0xC9,0xDF,0xD8,0xCF])
print(bytes(b ^ 0xAA for b in enc).decode())
EOF
# super secure
```

Même résultat en CyberChef : opération `From Hex` sur `D9DFDACFD88AD9CFC9DFD8CF`, puis `XOR` avec
`AA`.

### 3. Variante sans reversing : casser sur `strcmp`

```bash
lldb ./bypassme.bin
(lldb) breakpoint set --name strcmp
(lldb) run
# saisir n'importe quoi, puis :
(lldb) register read rsi
(lldb) memory read --format s $rsi     # → "super secure"
```

`strcmp` reçoit en `rdi` la saisie et en `rsi` la valeur attendue : le second argument est le mot de
passe en clair. Sous `gdb`, l'équivalent est `break strcmp` puis `x/s $rsi`.

### 4. Se reconnecter et lancer le binaire

```bash
ssh -p <PORT> ctf-player@<HOST>
./bypassme.bin
# Password: super secure
```

Le binaire setuid lit alors le fichier de flag et l'affiche.

### Pourquoi ça marche

Le XOR avec une clé constante est involutif : `b ^ k ^ k = b`. Le mot de passe est donc entièrement
reconstructible à partir du binaire, sans aucune recherche. Et même sans lire le code, le débogueur
montre la valeur au moment exact où elle est comparée : obfusquer une constante ne protège pas une
constante.

## Pièges

- **Exécuter la copie locale.** Sans le bit setuid effectif, la lecture du fichier de flag échoue : il
  faut lancer le binaire sur la machine distante.
- **Oublier le préfixe du compte.** Le `scp` se fait avec le compte fourni et le port SSH indiqué ;
  une erreur de port donne un `Connection refused` trompeur.
- **Se tromper de clé.** `0xAA` et non `0xAB` : un octet de différence et le mot de passe est
  illisible, ce qui ressemble à une mauvaise piste alors que c'est une faute de frappe.
- **Mal recopier les 12 octets.** Le tableau fait exactement 12 entrées, la dernière est `0xCF` ;
  un octet manquant décale la chaîne.
- **Le mot de passe contient une espace.** Si la saisie passe par un `%s`, l'espace coupe la valeur :
  vérifier le format de lecture dans le décompilé avant de conclure que le mot de passe est faux.
- **Passer le mot de passe en argument du shell.** Les guillemets sont nécessaires :
  `./bypassme.bin` puis saisie interactive reste le plus sûr.
