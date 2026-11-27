# 761 — Bypass Me

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Your task is to analyze and exploit a password-protected binary called `bypassme.bin`. The binary
> performs input sanitation. Instead of guessing the password, reverse engineer or debug the program
> to bypass the authentication logic and retrieve the hidden flag.

Le binaire est un exécutable **setuid** sur la machine distante (accès SSH fourni).

## Analyse

`main()` appelle `decode_password()` avant la séquence d'introduction : cette fonction prend 12
octets codés en dur et les XOR un par un avec la clé fixe `0xAA` pour produire le mot de passe
attendu — un simple obfuscation, pas du chiffrement. Deux voies équivalentes : décompiler (Ghidra)
et recalculer, ou laisser le binaire décoder en mémoire et lire la valeur au moment de la
comparaison. Comme le binaire est setuid, c'est sur la machine distante qu'il faut l'exécuter pour
lire le flag.

## Solution

1. Récupérer le binaire pour l'analyser : `scp -P <PORT> ctf-player@<HOST>:bypassme.bin .`
2. Décompiler et repérer `decode_password()` : 12 octets
   `D9 DF DA CF D8 8A D9 CF C9 DF D8 CF` XOR `0xAA`.
3. Décoder (CyberChef : `From Hex` puis `XOR` avec `AA`) → mot de passe `super secure`.
4. Variante sans reversing : casser sur `strcmp` et lire le second argument.

```bash
lldb ./bypassme.bin
(lldb) breakpoint set --name strcmp
(lldb) run
# saisir n'importe quoi, puis :
(lldb) register read rsi
(lldb) memory read --format s $rsi     # → "super secure"
```

5. Se reconnecter en SSH et lancer `./bypassme.bin` avec ce mot de passe : le binaire setuid lit le
   fichier de flag.

## Flag

```
picoCTF{d3bugg3r_p0w3r_is_4w3s0m3_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — Bypass Me (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-bypass-me)
- [far17sya/picoCTF-2026-Writeups — reverse-engineering/bypass-me](https://github.com/far17sya/picoCTF-2026-Writeups/blob/main/reverse-engineering/bypass-me/README.md)
- [snwau/picoCTF-2026-Writeup — Reverse Engineering/Bypass Me](https://github.com/snwau/picoCTF-2026-Writeup/blob/main/Reverse%20Engineering/Bypass%20Me/Bypass%20Me.md)
