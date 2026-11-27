# 528 - M1n10n'5_53cr37  (Reverse Engineering, picoMini by CMU-Africa)
# Flag: academy{1t_w4sn7_h4rd_unr4v3l1n9_th3_m0b1l3_c0d3}
# Write-up: ../../../writeups/reverse-engineering/528-m1n10n-5-53cr37.md
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


f = "academy{1t_w4sn7_h4rd_unr4v3l1n9_th3_m0b1l3_c0d3}"
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"528 M1n10n'5_53cr37 -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(528, "M1n10n'5_53cr37", "Reverse Engineering",
             "https://challenge-files.cylabacademy.net/library/.../minions.apk",
             "flag en Base32 dans une string resource Android", f,
             "APK de 5,9 Mo (package `com.example.picoctfimage`). Recherche infructueuse du motif "
             "`academy{` en clair dans TOUTES les entrees du zip (dex, ressources, arsc) : le drapeau "
             "est encode. Le code de l'app (`classes3.dex`) est trivial — une `MainActivity` qui fait "
             "`setContentView` et un listener d'insets — et la seule ressource graphique propre est "
             "`res/drawable/minion.jpg` (800x711, sans donnee apres EOI ni commentaire JPEG, donc pas de "
             "stegano triviale). Le drapeau se trouve en realite dans `res/values/strings.xml`, dans une "
             "ressource au nom anodin `Banana` dont la valeur est du **Base32** : "
             "`MFRWCZDFNV4XWMLUL53TI43OG5PWQNDSMRPXK3TSGR3DG3BRNY4V65DIGNPW2MDCGFWDGX3DGBSDG7I=`, "
             "qui se decode en `academy{1t_w4sn7_h4rd_unr4v3l1n9_th3_m0b1l3_c0d3}`. Methode : "
             "`apktool d` pour decoder les ressources binaires (le manifest et les valeurs sont en XML "
             "binaire, illisibles directement), puis lecture de `res/values/strings.xml`. Lecon : dans "
             "une APK, penser aux string resources obfusquees (base32/base64) et pas seulement au dex.")
