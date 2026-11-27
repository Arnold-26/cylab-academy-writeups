# 697 — The Add/On Trap

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé
« What kind of information can an Add/On reach? Is it possible to exfiltrate them without you
noticing? »

On récupère `suspicious.zip`, protégée par le mot de passe `picoctf`. À l'intérieur, une extension
de navigateur à inspecter : le flag est caché quelque part dans le code de l'add-on, et l'énoncé
suggère que la fuite passe par un canal discret.

## Analyse

### Déballer l'archive dans le bon ordre
Premier réflexe : `file` et `unzip -l` sur l'archive. On découvre qu'elle ne contient pas
l'arborescence attendue d'une extension, mais un unique fichier :
`56102ec0438646c68605-1.0.xpi`. L'extension `.xpi` est le format de paquetage des extensions
Firefox : c'est un ZIP renommé. Il faut donc extraire **deux fois**, et c'est le premier piège de
l'épreuve — beaucoup s'arrêtent au premier `unzip` et cherchent le flag dans un binaire opaque.

Après la double extraction, on obtient une arborescence lisible :

```
manifest.json
background/main.js
assets/script.js
popup.html
META-INF/            # signatures de l'extension
```

### Le manifeste ne dit rien, le background dit tout
`manifest.json` ne contient que des permissions et des points d'entrée : rien d'exploitable
directement, mais il confirme le modèle d'exécution (un script de fond persistant). C'est dans
`background/main.js` que se trouvent les deux constantes intéressantes :

- `key`, une chaîne base64 de 44 caractères se terminant par `=` :
  `cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0=`. Décodée, elle donne un texte au format du flag,
  mais **tronqué en plein mot** et long de exactement 32 octets. C'est un leurre volontaire : le
  challenge veut qu'on s'arrête là et qu'on soumette une valeur incomplète.
- `webhookUrl`, qui n'est pas une URL mais un **jeton Fernet**. Tous les jetons Fernet commencent
  par `gAAAAA` (version `0x80`, timestamp Unix sur 8 octets), ce qui les rend immédiatement
  reconnaissables, même noyés dans un champ qui prétend être une URL.

Un commentaire du fichier ajoute que la clé doit faire « 32 url-safe base64 bytes ». La chaîne
tronquée fait précisément 32 octets une fois décodée : ce n'est donc pas un flag, c'est une **clé
Fernet**, et le jeton est le chiffré qu'elle ouvre. Le raisonnement se referme : le leurre est en
réalité le matériel cryptographique.

## Solution

### Extraction et repérage
```bash
unzip -P picoctf suspicious.zip
# produit 56102ec0438646c68605-1.0.xpi
unzip 56102ec0438646c68605-1.0.xpi -d suspicious/
grep -rn 'picoCTF' suspicious/          # ne donne rien d'utile : le flag est chiffré
grep -rnE 'key|webhook|gAAAAA' suspicious/background/
```

### Décodage de la constante
```bash
python3 -c "import base64; print(base64.b64decode('cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0='))"
python3 -c "import base64; print(len(base64.b64decode('cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0=')))"
# 32
```

### Déchiffrement Fernet
```bash
pip install cryptography
python3 - <<'PY'
from cryptography.fernet import Fernet
k = b'cGljb0NURnt5b3UncmUgb24gdGhlIHJpZ2h0IHRyYX0='
t = b'gAAAAABmfRjwFKUB-X3GBBqaN1tZYcPg5oLJVJ5XQHFogEgcRSxSis1e4qwicAKohmjqaD-QG8DIN5ie3uijCVAe3xiYmoEHlxATWUP3DC97R00Cgkw4f3HZKsP5xHewOqVPH8ap9FbE'
print(Fernet(k).decrypt(t).decode())
PY
```

Le déchiffrement affiche le flag complet. On le soumet tel quel : c'est la sortie du déchiffrement,
pas la constante base64 du fichier.

### Pourquoi ça marche
Fernet n'est pas un chiffrement exotique : c'est un conteneur normalisé, **AES-128-CBC** pour la
confidentialité plus **HMAC-SHA256** pour l'intégrité, avec une clé de 32 octets encodée en base64
url-safe. Le jeton embarque la version, l'horodatage, l'IV, le chiffré et le tag HMAC. Dès lors
qu'on possède la clé — et elle est dans le JavaScript de l'extension — le déchiffrement est
purement mécanique : aucune attaque cryptographique n'est nécessaire. Le « piège » du challenge est
un piège d'**interprétation**, pas de cryptanalyse : il faut comprendre que la chaîne tronquée n'est
pas une réponse mais un outil.

C'est aussi la leçon de fond de l'épreuve, et elle est énoncée dans le titre : une extension ne peut
pas garder de secret. L'utilisateur reçoit le code, donc la clé, donc le clair. Tout le modèle de
sécurité d'un add-on repose sur la confiance dans le code livré, jamais sur une valeur cachée à
l'intérieur de ce code.

## Pièges
- **Ne pas s'arrêter au premier `unzip`** : le `.xpi` est une archive imbriquée. Sans la seconde
  extraction, on n'a qu'un blob et on passe à côté des sources.
- **Le faux flag** : la constante base64 décodée ressemble à une réponse complète. Sa longueur de
  32 octets et sa troncature en plein mot sont les deux signaux qui doivent alerter. Soumettre cette
  valeur échoue.
- **Ne pas confondre les deux objets** : `webhookUrl` contient un jeton, pas une URL. Un `grep url`
  ou un `curl` sur ce champ ne mène à rien.
- **Garder le padding `=`** de la clé : `Fernet()` exige une clé base64 de 32 octets décodés ;
  retirer le `=` casse le décodage. De même, le jeton doit être manipulé comme des octets
  (`b'...'`), pas comme une chaîne dont on aurait normalisé les caractères.
- **Version de `cryptography`** : l'API `Fernet(key).decrypt(token)` est stable, mais un jeton
  expiré ou un `ttl` mal placé lève une exception — ici on n'active pas de TTL, le jeton est ancien.

## Flag

Flag validé sur la plateforme (valeur non conservée).
