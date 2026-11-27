import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "picoCTF{styl1ng_susp1c10usly_s1m1l4r_t0_p4steb1n}"
st, b = cy.req("GET", "/api/challenges/204/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 204, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"204 notepad (deja={already}) -> {ok}")
if ok and not already:
    wu.write(204, "notepad", "Web Exploitation", "https://notepad.mars.cylabacademy.net",
             "path traversal backslash + SSTI sans underscore", f,
             "Le filtre ne bloque que `/` et `_`, mais `werkzeug.url_fix` convertit **`\\` en `/` "
             "APRES** le filtre. Contenu `\\..\\templates\\errors\\<nom><payload>` ecrit donc dans "
             "`templates/errors/`, puis `?error=<nom>-<token>` fait rendre le fichier par Jinja -> SSTI. "
             "Le blocage `_` se contourne sans underscore : `{%set u=(config|string)[74]%}` extrait "
             "l'underscore de la repr de `config` (index 74 = le premier `_`), puis "
             "`attr(u*2+'class'+u*2)` etc. Piege : extraire le nom du fichier depuis le header "
             "`Location` avec `rsplit('-',1)` casse tout car le token `token_urlsafe` contient lui-meme "
             "des tirets ; il faut prendre tout ce qui suit le dernier `/`.")
