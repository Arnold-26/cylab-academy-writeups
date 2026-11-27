# 700 — Binary Instrumentation 4

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

« The executable was designed to send the flag to someone. Are you that someone? »

`bin-ins4.zip` (mot de passe `picoctf`) livre `bin-ins4.exe`, qui prétend envoyer le flag à un
destinataire distant. La consigne précise qu'il faut l'exécuter avec un **listener local sur le port
9867**.

## Analyse

### Le binaire ne parle à personne d'atteignable
Avec un `ncat` en écoute, rien n'arrive. La destination est **codée en dur** : `192.168.29.25:9867`,
une adresse d'un réseau local qui n'existe pas chez nous. Le `connect()` échoue et le programme ne se
plaint pas — il considère que l'envoi a été tenté.

Second verrou avant l'envoi : une invite « Enter the key » compare la saisie à une valeur attendue.

### Deux hooks suffisent
Le binaire est packé et peu lisible en statique, mais il appelle des API Windows connues :

1. **`ws2_32!connect`** — le second argument est un pointeur vers une `sockaddr_in`. En réécrivant
   l'adresse et le port **dans la structure** en `onEnter`, on détourne la connexion vers
   `127.0.0.1:9867`. Le noyau lit la structure **après** le retour du hook : la modification en place
   est prise en compte sans changer la valeur de retour de `connect`.
2. **`kernel32!lstrcmpA`** — la vérification de la clé passe par cette comparaison. Forcer le retour à
   `0` en `onLeave` fait accepter n'importe quelle clé.

Une fois la clé « validée », le programme envoie le flag sur la socket, sous forme de chaîne base64.

## Solution

```bash
unzip -P picoctf bin-ins4.zip
ncat -lvp 9867                      # listener à lancer AVANT le binaire
```

### Étape 1 — confirmer la destination
```javascript
// discover.js
const connect = Module.getExportByName('ws2_32.dll', 'connect');
Interceptor.attach(connect, {
  onEnter(args) {
    const sa = args[1];
    const port = (sa.add(2).readU8() << 8) | sa.add(3).readU8();
    const ip = [0,1,2,3].map(i => sa.add(4 + i).readU8()).join('.');
    console.log(`connect() ${ip}:${port}`);
  }
});
```
```bash
frida -f bin-ins4.exe -l discover.js --no-pause
# connect() 192.168.29.25:9867
```

### Étape 2 — rediriger la connexion
```javascript
// redirect.js
const connect = Module.getExportByName('ws2_32.dll', 'connect');
Interceptor.attach(connect, {
  onEnter(args) {
    const sa = args[1];
    sa.writeU16(2);                                       // AF_INET
    sa.add(2).writeByteArray([0x26, 0x8b]);               // port 9867 en réseau
    sa.add(4).writeByteArray([0x7f, 0x00, 0x00, 0x01]);   // 127.0.0.1
  }
});
```

Le port s'écrit en **big-endian** : 9867 vaut `0x268b`, donc les octets `26 8b`. En little-endian on
obtiendrait `8b 26`, soit le port 35622, et le listener ne verrait rien.

### Étape 3 — accepter n'importe quelle clé
```javascript
// solve.js : redirect + neutralisation de la comparaison
const connect  = Module.getExportByName('ws2_32.dll', 'connect');
const lstrcmpA = Module.getExportByName('kernel32.dll', 'lstrcmpA');

Interceptor.attach(connect, {
  onEnter(args) {
    const sa = args[1];
    sa.writeU16(2);
    sa.add(2).writeByteArray([0x26, 0x8b]);
    sa.add(4).writeByteArray([0x7f, 0x00, 0x00, 0x01]);
  }
});
Interceptor.attach(lstrcmpA, { onLeave(retval) { retval.replace(0); } });
```
```bash
frida -f bin-ins4.exe -l solve.js --no-pause
# taper une clé quelconque ; le listener affiche le blob base64
echo '<blob_b64_affiche_par_ncat>' | base64 -d
```

### Variante statique
On a aussi reconstitué le flag sans exécuter le binaire : la charge utile est dans `.ATOM`,
compressée ; on la décompresse, puis on lit le code de `lstrcmpA` et la construction de la chaîne
base64, ce qui permet de recoller les fragments à la main.

### Pourquoi ça marche
`connect()` ne décide de rien : il passe au noyau la `sockaddr` qu'on lui donne. En la mutant avant
l'appel système, on change la destination sans patcher une seule instruction — on corrige un
**argument**. Le second hook relève de la même logique : le programme teste le retour de `lstrcmpA`
contre zéro, on remplace la valeur, donc le test réussit quel que soit l'entrée. Aucun des deux ne
demande de connaître la clé ou l'adresse réelle.

## Pièges

- **Structure `sockaddr_in`** : famille `u16`, port `u16` **réseau**, adresse sur 4 octets, puis 8
  octets de zéro. Un offset faux décale tout.
- **Endianness du port** : l'erreur la plus fréquente. `writeU16(9867)` écrit en little-endian et
  produit un port différent.
- **`onEnter` vs `onLeave`** : `sockaddr` en `onEnter`, neutralisation de `lstrcmpA` en `onLeave`.
- **Ordre de lancement** : le listener écoute avant que le binaire ne se connecte ; le lancer après ne
  sert à rien, et `--no-pause` est nécessaire pour que Frida ne suspende pas le processus.

## Flag

Flag validé sur la plateforme (valeur non conservée).
