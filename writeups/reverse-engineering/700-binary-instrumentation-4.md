# 700 — Binary Instrumentation 4

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« The executable was designed to send the flag to someone. Are you that someone? » Le binaire
`bin-ins4.zip` (mot de passe `picoctf`) doit être exécuté avec un listener local sur le port 9867.

## Analyse
Le programme ouvre une connexion TCP vers une destination **codée en dur** — `192.168.29.25:9867`
selon les writeups publics — évidemment injoignable, donc le flag n'arrive jamais. Deux hooks
Frida suffisent :

1. `ws2_32!connect` : le second argument est un `sockaddr_in` ; en réécrivant l'adresse (et le port)
   dans la structure en `onEnter`, le noyau connecte vers `127.0.0.1:9867`. Comme la structure est
   lue après le retour du hook, la modification en place est prise en compte.
2. `kernel32!lstrcmpA` : la vérification de la clé passe par cette comparaison ; forcer la valeur
   de retour à 0 en `onLeave` fait accepter n'importe quelle clé (« Enter the key »).

Une fois la clé « validée », le programme envoie le flag sur la socket sous forme de chaîne base64.

## Solution
```bash
unzip -P picoctf bin-ins4.zip
ncat -lvp 9867                     # listener à lancer AVANT le binaire
frida -f bin-ins4.exe -l discover.js --no-pause   # log de connect(): IP + port
frida -f bin-ins4.exe -l redirect.js --no-pause   # réécriture du sockaddr
frida -f bin-ins4.exe -l solve.js --no-pause      # redirect + lstrcmpA -> 0
# taper une clé quelconque, le listener affiche le blob base64 :
echo 'cGljb0NURntuM3R3MHJrXzFzXzRQMXNfNFNfVzMxMV8uLi59Cg==' | base64 -d
```
Un autre writeup arrive au même résultat par analyse statique : payload packé dans `.ATOM`,
décompression, lecture de la logique `lstrcmpA` et reconstruction des fragments base64.

## Flag
```
picoCTF{n3tw0rk_1s_4P1s_4S_W311_6ae41cdc}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-binary-instrumentation-4 — page de solution picoCTF 2026 (hooks `connect`/`lstrcmpA`, chaîne base64)
- https://cyb3r-bo1.github.io/posts/picoCTF_2026_writeup/ — writeup picoCTF 2026 (flag complet, voie statique)
