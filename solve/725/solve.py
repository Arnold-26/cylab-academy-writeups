# 725 - North-South  (Web Exploitation, picoCTF 2026)
# Flag: academy{g30_b453d_r0u71n9_5e58725f}
# Write-up: ../../../writeups/web-exploitation/725-north-south.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{g30_b453d_r0u71n9_5e58725f}"
st, b = cy.req("GET", "/api/challenges/725/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 725, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"725 North-South (deja={already}) -> {ok}")
if ok and not already:
    wu.write(725, "North-South", "Web Exploitation", "http://chatelaine.cylabacademy.net:<port>/",
             "geo-routing nginx contourne par un exit Tor islandais", f,
             "Le service nginx route selon le pays GeoIP2 : la config fournie montre "
             "`geoip2 /etc/nginx/GeoLite2-Country.mmdb { $geoip2_data_country_code default=ZZ country "
             "iso_code; }` puis, dans `location /`, `if ($geoip2_data_country_code = IS) { proxy_pass "
             "http://south; }` et sinon `proxy_pass http://north;`. Seuls les visiteurs ISLANDAIS "
             "(code ISO `IS`) atteignent le serveur qui detient le drapeau. **Aucun en-tete n'est "
             "utilise** : pas de module `real_ip`, pas de `set_real_ip_from`, donc `X-Forwarded-For` "
             "et `X-Real-IP` sont sans effet (verifie dans la config, contre ce que suggerent certains "
             "writeups). Il faut donc une VRAIE adresse islandaise : j'ai lance Tor avec "
             "`ExitNodes {is}` et `StrictNodes 0`, attendu le bootstrap complet (~3 min, le consensus "
             "etait lent), verifie l'exit via un service de geolocalisation, puis requete le service "
             "avec `curl --socks5-hostname 127.0.0.1:9050` (le suffixe `h` est indispensable pour que "
             "la resolution DNS soit deleguee a Tor). La page renvoie alors le drapeau au lieu de "
             "« No flag in this region ».")
