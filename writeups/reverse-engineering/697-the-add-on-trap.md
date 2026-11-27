# 697 — The Add/On Trap

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« What kind of information can an Add/On reach? Is it possible to exfiltrate them without you
noticing? » L'archive `suspicious.zip` (mot de passe `picoctf`) contient une extension de
navigateur à inspecter pour retrouver le flag caché.

## Analyse
L'archive protégée ne contient pas l'arborescence de l'extension mais un unique fichier
`56102ec0438646c68605-1.0.xpi`, qui est lui-même un ZIP (une extension Firefox). Après double
extraction on obtient `manifest.json`, `background/main.js`, `assets/script.js`, `popup.html` et
les fichiers de signature `META-INF/`.

Le manifeste ne contient que des permissions et des points d'entrée ; c'est dans
`background/main.js` que se trouvent deux constantes intéressantes :

- `key = "cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0="`, du base64 qui décode en
  `picoCTF{you're on the right tra}` : un **faux flag** volontairement tronqué en plein mot, et
  long de exactement 32 octets ;
- `webhookUrl`, qui n'est pas une URL mais un **jeton Fernet** (tout jeton Fernet commence par
  `gAAAAA`).

Un commentaire du fichier précise que la clé doit faire « 32 url-safe base64 bytes » : la chaîne
tronquée est donc une clé Fernet, et le jeton est le chiffré qu'elle ouvre.

## Solution
```bash
unzip -P picoctf suspicious.zip
unzip 56102ec0438646c68605-1.0.xpi -d suspicious/
grep -rn 'picoCTF' suspicious/
```
On décode la constante, puis on déchiffre le jeton :
```bash
python3 -c "import base64;print(base64.b64decode('cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0='))"
pip install cryptography
python3 -c "from cryptography.fernet import Fernet; k=b'cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0='; t=b'gAAAAABmfRjwFKUB-X3GBBqaN1tZYcPg5oLJVJ5XQHFogEgcRSxSis1e4qwicAKohmjqaD-QG8DIN5ie3uijCVAe3xiYmoEHlxATWUP3DC97R00Cgkw4f3HZKsP5xHewOqVPH8ap9FbE'; print(Fernet(k).decrypt(t).decode())"
```
Le déchiffrement Fernet (AES-128-CBC + HMAC-SHA256) affiche le flag complet. Leçon : une extension
ne peut pas garder de secret, puisque l'utilisateur reçoit le code et donc la clé.

## Flag
```
picoCTF{Us3_4dd/0ns_v3r4_c4r3fully1}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-the-add-on-trap — page de solution picoCTF 2026 (énoncé, étapes Frida/Fernet, faux flag)
- https://zhienw.com/post/the_add_on_trap/ — writeup indépendant du même challenge (flag complet)
