import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
u = "https://picoctfsolutions.com/picoctf-2021-cache-me-outside"
r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
print("taille:", len(t))
# toutes les occurrences de picoCTF{ avec contexte large
for m in re.finditer(r"picoCTF\{", t):
    seg = t[m.start():m.start()+220]
    seg = seg.replace("\\u0026", "&")
    print("---")
    print(seg[:220])
# chercher un JSON __NEXT_DATA__
m = re.search(r'__NEXT_DATA__[^>]*>(.*?)</script>', t, re.S)
print("NEXT_DATA present:", bool(m))
if m:
    print("longueur next data:", len(m.group(1)))
    for mm in re.finditer(r"picoCTF\{[^}]{0,200}", m.group(1)):
        print("  ND:", mm.group(0)[:200])
