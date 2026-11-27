# 699 — Binary Instrumentation 3

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« The executable was designed to write the flag but it seems like a few things went wrong. Can you
find a way to get it to work? » Le binaire Windows `bin-ins3.exe` est fourni dans `bin-ins3.zip`
(mot de passe `picoctf`).

## Analyse
Le PE est **packé** : le fichier sur disque n'est qu'un stub qui décompresse une charge utile en
mémoire, puis transfère l'exécution. Le programme devrait écrire le flag dans
`C:\random\output_flag.txt`, mais le fichier produit contient des déchets.

La raison est une routine **d'effacement d'en-tête** du packer (`sub_1400015A0` d'après IDA) :
juste après l'expansion du payload, elle met à zéro les premiers octets (MZ/PE) de l'image en
mémoire, pour empêcher un dump naïf. Toute recherche statique de chaîne échoue donc : le flag
n'existe qu'en mémoire et sous forme base64.

## Solution
```bash
unzip -P picoctf bin-ins3.zip
file bin-ins3.exe
./bin-ins3.exe          # constate l'échec, puis ouvre le binaire dans Ghidra/IDA
pip install frida-tools
frida-trace .\bin-ins3.exe -I 'bin-ins3.exe'   # repère l'appel juste avant le transfert au payload
```
Ensuite un script Frida `dump_payload.py` qui *spawn* le processus, hooke la fonction
d'effacement, lit `SizeOfImage` dans l'en-tête optionnel du PE (offset `+0x38` après `PE + 0x18`),
copie `SizeOfImage` octets avant l'effacement et les écrit sur disque :
```bash
python dump_payload.py
strings payload_dumped.exe | grep -i 'picoctf\|cGljb0'
echo 'cGljb0NURnt...' | base64 -d
```
Le dump est un PE valide dont les chaînes contiennent le flag en base64. Alternative documentée
par un autre writeup : décompresser statiquement la section `.ATOM` (LZMA) puis concaténer les
fragments base64 des constructeurs statiques.

## Flag
```
picoCTF{411_4r3_4p15_n07h1n9_3l53_4f70640e}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-binary-instrumentation-3 — page de solution picoCTF 2026 (liaison vérifiée vers `learn.cylabacademy.org/library/699`)
- https://cyb3r-bo1.github.io/posts/picoCTF_2026_writeup/ — writeup picoCTF 2026 (flag complet, voie statique `.ATOM`/LZMA)
