# 717 — Silent Stream

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« We recovered a suspicious packet capture file that seems to contain a transferred file. The
sender was kind enough to also share the script they used to encode and send it. Can you
reconstruct the original file? » Fichiers : `packets.pcap` et `encrypt.py`.

## Analyse
`encrypt.py` montre un encodage par **décalage additif** : chaque octet est décalé de 42 modulo 256,
soit `encoded = (original + 42) % 256`. Le fichier encodé a simplement été envoyé sur le réseau et
capturé.

Le piège est de ne pas dumper tout le PCAP d'un coup (les flux TCP s'entremêlent et produisent des
déchets) mais d'isoler **le bon flux TCP** : `Follow → TCP Stream`, affichage en `Raw`, puis copie du
contenu hexadécimal. Le décodage est l'inverse arithmétique : `original = (encoded - 42) % 256`.

Le résultat est un blob binaire dont le type s'identifie avec `file` : ici une image **JPEG**
(800×500) sur laquelle le flag est écrit en rouge au milieu d'une image par ailleurs blanche.

## Solution
```bash
cat encrypt.py
wireshark packets.pcap &
# clic droit sur un paquet du bon flux -> Follow -> TCP Stream -> "Show data as: Raw"
# copier le contenu hexadécimal dans silentstream.hex
xxd -r -p silentstream.hex decoded.bin      # hex -> octets
python3 - <<'EOF'
data = open('decoded.bin','rb').read()
open('recovered','wb').write(bytes((b - 42) % 256 for b in data))
EOF
file recovered        # JPEG
mv recovered decoded.jpg && xdg-open decoded.jpg
```

## Flag
```
picoCTF{tr4ck_th3_tr4ff1c_c1f1c1d9}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-silent-stream — page de solution picoCTF 2026 (décalage +42, extraction du flux TCP, JPEG)
- https://ankur-gautam.gitbook.io/writeups/reverse-engineering/reverse-engineering-ctf-writeups/picoctf/silent-stream — writeup dédié au challenge Silent Stream (flag complet)
