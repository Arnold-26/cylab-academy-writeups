# 732 — KSECRETS

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé
« We have a kubernetes cluster setup and the flag is in the secrets. You think you can get it? »

Après lancement de l'instance, un fichier `kubeconfig.yaml` est fourni : il contient les
identifiants et l'adresse du cluster. Le flag est stocké dans un objet **Secret** Kubernetes.

## Analyse

### Le principe
Kubernetes organise ses objets par **namespace**. Un `Secret` est un objet qui contient des paires
clé/valeur destinées à porter des données sensibles : mots de passe, jetons, certificats. Par
défaut, ces objets ne sont **pas chiffrés au repos** : ils sont seulement **encodés en base64**.
N'importe quel principal disposant du droit `list`/`get` sur les secrets d'un namespace peut donc
lire leur contenu en clair après un simple décodage.

C'est un point souvent mal compris : base64 n'est pas du chiffrement, c'est un encodage de transport.
Il ne protège rien — il rend seulement les données compactes et sûres à passer dans du JSON/YAML.

### Le piège du namespace
Premier réflexe :

```bash
export KUBECONFIG=./kubeconfig
kubectl get secrets
```

La commande ne renvoie rien, ou seulement les secrets techniques par défaut. Le namespace courant du
kubeconfig est `default`, et le flag n'y est pas. Il faut chercher **partout**, avec `-A`
(`--all-namespaces`). C'est là qu'apparaît un secret nommé `ctf-secrets` (ou `ctf-secret` selon
l'instance) dans un namespace dédié, `picoctf`, avec une clé `flag`.

Deuxième point, spécifique aux instances régénérées : le `server:` du kubeconfig peut pointer sur une
URL qui n'est plus la bonne, ou sur un nom d'hôte dont le certificat ne correspond pas. Il faut alors
réécrire cette ligne avec l'URL de l'instance (`https://<host>:<port>`) et ajouter
`--insecure-skip-tls-verify=true` pour ne pas buter sur la validation du certificat.

## Solution

### Mise en place
```bash
export KUBECONFIG=./kubeconfig
kubectl config view --minify
kubectl get namespaces --insecure-skip-tls-verify
```

Si `kubectl` renvoie une erreur de certificat ou d'hôte inconnu, corriger l'URL :

```bash
sed -i 's|^\(\s*server:\).*|\1 https://<host>:<port>|' kubeconfig.yaml
```

### Chercher partout
```bash
kubectl get secrets -A --insecure-skip-tls-verify
```

La sortie liste les secrets de tous les namespaces. On repère celui dont le nom parle de CTF, dans le
namespace `picoctf`.

### Lire et décoder
```bash
kubectl get secret ctf-secrets -n picoctf --insecure-skip-tls-verify -o yaml
kubectl get secret ctf-secrets -n picoctf --insecure-skip-tls-verify \
        -o jsonpath='{.data.flag}' | base64 -d ; echo
```

La valeur renvoyée par `jsonpath` est la chaîne base64 **du champ `data`** : elle est directement
décodable. Attention à ne pas la confondre avec `stringData`, qui contient la valeur en clair.

Variantes utiles :

```bash
# tout le secret, en clair, quel que soit le nom des clés
kubectl get secret ctf-secrets -n picoctf --insecure-skip-tls-verify -o json \
  | jq -r '.data | to_entries[] | .value' | while read v; do echo "$v" | base64 -d; echo; done

# vérifier ses droits avant de chercher
kubectl auth can-i list secrets -n picoctf --insecure-skip-tls-verify
```

### Pourquoi ça marche
Un `Secret` Kubernetes n'est qu'un objet de configuration un peu mieux traité : l'API le stocke dans
etcd, encodé en base64 pour rester du JSON valide. Sans configuration explicite de chiffrement au
repos (`EncryptionConfiguration` côté kube-apiserver), les données sont lisibles par quiconque
dispose du RBAC adéquat. Le challenge distribue un kubeconfig avec des droits suffisants : la seule
difficulté est de **savoir où regarder** — un namespace précis, avec un nom qu'on ne devine pas. Le
`-A` transforme une recherche aveugle en énumération exhaustive.

## Pièges
- **Oublier `-A`** : le namespace `default` ne contient rien. C'est le piège principal, et il fait
  perdre beaucoup de temps si l'on ne sait pas que Kubernetes cloisonne par namespace.
- **`kubectl get secrets` sans `-n`** : idem, on reste sur le namespace courant du contexte.
- **Erreur TLS** : le kubeconfig fourni peut avoir un `server:` obsolète ou un certificat
  auto-signé. `--insecure-skip-tls-verify` est la soupape, à utiliser sciemment.
- **Décoder deux fois** : `-o yaml` affiche déjà la valeur base64 du champ `data`. Un `base64 -d` sur
  la sortie complète du YAML ne donne rien — il faut cibler le champ.
- **`stringData` vs `data`** : le premier est en clair (et n'est pas toujours présent), le second est
  en base64. Confondre les deux fait décoder du texte déjà lisible.
- **Nom variable** : `ctf-secrets` ou `ctf-secret` d'une instance à l'autre. Un `grep -i ctf` sur la liste
  évite de supposer.

## Flag

Flag validé sur la plateforme (valeur non conservée).
