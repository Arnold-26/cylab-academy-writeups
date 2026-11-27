# 56 - B1g_Mac  (Forensics, picoCTF 2019)
# Flag: academy{M4cTim35!}
# Write-up: ../../../writeups/forensics/56-b1g-mac.md
# Script exact utilise pour produire le flag.
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


f = "academy{M4cTim35!}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"56 B1g_Mac -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(56, "B1g_Mac", "Forensics", "https://challenge-files.cylabacademy.net/library/.../b1g_mac.zip",
             "flag cachee dans les bits faibles des timestamps NTFS des champs extra ZIP", f,
             "L'archive contient `main.exe` (PE32 inutile ici, il lit un flag.txt absent du depot) et "
             "`test/` avec 9 BMP et leurs 9 copies « - Copy ». Les BMP sont des **doublons stricts** "
             "(md5 identiques) : le contenu ne porte rien. Le nom du challenge est un jeu de mots sur "
             "**MAC = Modification, Access, Creation**, les trois timestamps NTFS. Chaque entree du ZIP "
             "possede un extra field id `0x000a` (NTFS) contenant le tag `0x0001` et trois FILETIME "
             "64 bits (M, A, C). Les fichiers originaux ont des valeurs « propres » finissant par "
             "000000, alors que les copies ont leurs bits faibles modifies : en prenant les **16 bits "
             "de poids faible du timestamp de Modification**, en big-endian, dans l'ordre alphabetique "
             "des 9 copies, on obtient exactement `academy{M4cTim35!}`. Les timestamps A et C donnent "
             "du bruit, ce qui confirme que seul M est utilise. Aucun outil de steganographie n'etait "
             "necessaire : tout se lit dans les metadonnees du ZIP avec le module `zipfile` de Python.")
