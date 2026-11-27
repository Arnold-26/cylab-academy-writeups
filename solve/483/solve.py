# 483 - YaraRules0x100  (General Skills, picoCTF 2025)
# Flag: academy{yara_rul35_r0ckzzz_790c7af6}
# Write-up: ../../../writeups/general-skills/483-yararules0x100.md
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


f = "academy{yara_rul35_r0ckzzz_790c7af6}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"483 YaraRules0x100 -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(483, "YaraRules0x100", "General Skills", "socat - TCP:xebec.cylabacademy.net:<port>",
             "regle YARA soumise a un checker de 64 testcases (faux negatifs + faux positifs)", f,
             "Le zip (mot de passe `picoctf`) contient `suspicious.exe`, un PE32 **compresse UPX** : "
             "`strings` ne donne rien tant qu'on ne le decompresse pas avec `upx -d` (26 624 -> "
             "40 960 octets). Le binaire est un faux malware avec anti-debug, et l'enonce demande "
             "d'ecrire des regles YARA puis de les soumettre a un service (`socat - TCP:host:port`). "
             "Le protocole : envoyer le contenu de la regle puis fermer l'ecriture (EOF) ; le serveur "
             "teste la regle sur **64 cas** et rapporte separement les faux negatifs et les faux "
             "positifs. Pieges : un simple `condition: true` echoue en faux positif, et fermer la "
             "connexion trop vite apres l'envoi fait repondre « Your rulefile was empty » (il faut un "
             "court delai avant le shutdown). La regle gagnante combine le magic `{4D 5A}`, la chaine "
             "distinctive `YaraRules0x100`, `UPX`/`NtQuery`, et le motif large `debugger process`. "
             "Logique : exiger le magic PE plus un marqueur unique evite les faux positifs, tandis que "
             "la branche `$str5` couvre les variantes recompressees.")
