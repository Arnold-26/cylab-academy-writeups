# 458 - perplexed  (Reverse Engineering, picoCTF 2025)
# Flag: academy{0n3_bi7_4t_a_7im3}
# Write-up: ../../../writeups/reverse-engineering/458-perplexed.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""


f = "academy{0n3_bi7_4t_a_7im3}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"458 perplexed -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(458, "perplexed", "Reverse Engineering",
             "https://challenge-files.cylabacademy.net/library/.../perplexed", 
             "inversion d'une permutation de bits comparee octet par octet", f,
             "Binaire 64 bits non-PIE, 16 Ko. `main` lit un mot de passe avec `fgets` puis appelle "
             "`check`. `check` exige `strlen(buffer) == 0x1b` (27) — comme `fgets` conserve le saut de "
             "ligne, cela veut dire 26 caracteres utiles. Il construit ensuite un blob de 27 octets "
             "avec trois `movabs` (c3 8f 0e 4c bb 7c fb 61 | b9 9d fc 5a 5b df 69 d2 | d2 fe 1b ed f4 "
             "ed 67 f4), et compare **bit a bit** avec une double boucle : le blob utilise le masque "
             "`1 << (7-m)` et l'entree `1 << (7-j)`, avec `j` qui s'incremente deux fois plus vite et "
             "se remet a 0 en meme temps que l'indice d'entree avance. C'est donc une **permutation de "
             "bits** : le blob n'est pas le mot de passe mais ses bits reordonnes. Deux details "
             "trouves par l'experience : (1) j'avais d'abord inverse les deux masques, ce qui donnait "
             "des octets non imprimables ; (2) seuls **23 octets de blob** sont utilises (`cmp k,0x16`), "
             "donc les octets 23-26 du blob sont du remplissage inutilise (on y voyait `00 e8 df ff`, "
             "des restes de pile). En simulant exactement la boucle on retrouve "
             "`academy{0n3_bi7_4t_a_7im3}`, et le 27e octet doit etre `\\n` (0x0a), ce que le "
             "brute-force local des 256 valeurs a confirme immediatement.")
