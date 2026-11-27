# 732 — KSECRETS

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« We have a kubernetes cluster setup and the flag is in the secrets. You think you can get it? »
Un `kubeconfig.yaml` est fourni après lancement de l'instance.

## Analyse
Le challenge consiste à utiliser `kubectl` contre un cluster distant avec le kubeconfig fourni, puis
à chercher dans les **Secrets** Kubernetes. Les secrets ne sont pas chiffrés au repos par défaut :
ils sont seulement encodés en base64, donc lisibles par quiconque a le droit de les lister.

Le piège est le namespace : le namespace `default` ne contient rien. Il faut chercher partout
(`-A` / `--all-namespaces`), ce qui fait apparaître un secret `ctf-secrets` (ou `ctf-secret` selon
l'instance) dans le namespace `picoctf`, avec une clé `flag` en base64.

## Solution
```bash
export KUBECONFIG=./kubeconfig
kubectl get namespaces --insecure-skip-tls-verify        # si erreur de certificat
kubectl get secrets -A --insecure-skip-tls-verify        # tout voir
kubectl get secret ctf-secrets -n picoctf --insecure-skip-tls-verify -o yaml
kubectl get secret ctf-secrets -n picoctf --insecure-skip-tls-verify \
        -o jsonpath='{.data.flag}' | base64 -d
```
Un writeup note aussi qu'il faut parfois réécrire `server:` dans `kubeconfig.yaml` avec l'URL de
l'instance (`https://<host>:<port>`) et ajouter `--insecure-skip-tls-verify=true`.

## Flag
```
picoCTF{ks3cr375_41n7_s4f3_4013a368}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-ksecrets — page de solution picoCTF 2026 (`kubectl get secrets -A`, décodage base64)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (secret `ctf-secret` en base64, flag complet)
