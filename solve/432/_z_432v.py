import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{71m3_7r4v311ng_p1c7ur3_9490a52b}"
st, b = cy.req("GET", "/api/challenges/432/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 432, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"432 Blast from the past -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(432, "Blast from the past", "Forensics",
             "original.jpg + 2 services nc", "patch binaire des 7 tags EXIF a l'epoque Unix", f,
             "Challenge interactif : il faut soumettre une image MODIFIEE. `nc -w 2 <host> 11287 < "
             "image.jpg` ecrit `test.out`, puis `nc <host> 11534` (sans rien envoyer) valide et liste "
             "les 7 tags attendus : ModifyDate, DateTimeOriginal, CreateDate a "
             "`1970:01:01 00:00:00` ; SubSecCreateDate/SubSecDateTimeOriginal/SubSecModifyDate a "
             "`1970:01:01 00:00:00.001` ; et le tag Samsung TimeStamp a "
             "`1970:01:01 00:00:00.001+00:00` (tout fuseau equivalent accepte). **Piege principal : "
             "exiftool detruit la MakerNote Samsung** en reecrivant le fichier — resultat : 6/7 tags "
             "OK puis « Your picture doesn't have the Samsung: TimeStamp tag ». La solution est de "
             "**patcher les octets en place** (indice du challenge : « exiftool is really good at "
             "reading metadata, but you might want to use something else to modify it ») : les 3 "
             "chaines `2023:11:20 15:46:23` (offsets 398, 856, 876) -> `1970:01:01 00:00:00`, les 3 "
             "sous-secondes `703` (offsets 688, 700, 712) -> `001`, et surtout le TimeStamp Samsung, "
             "stocke en **ASCII a l'offset 0x2b83e0** sous forme d'epoch en millisecondes "
             "(`1700513181420`), a remplacer par `1` + NUL. `exiftool -v3` donne directement l'offset "
             "de ce tag (2b83e0) — c'est ce qui a permis de le trouver. Verification locale : "
             "`exiftool` affiche bien `Time Stamp : 1970:01:01 01:00:00.001+01:00`, equivalent a "
             "`00:00:00.001+00:00`.")
