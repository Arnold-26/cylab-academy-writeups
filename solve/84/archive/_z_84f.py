import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = "cccaaddemyemy{N0t_{StaTa_fLa31355g}_36f6e6e}"
print("longueur:", len(s))
print("even:", s[::2])
print("odd :", s[1::2])
# recherche de motifs
for i in range(len(s)):
    for j in range(i + 5, len(s) + 1):
        sub = s[i:j]
        if sub.startswith("{") and sub.endswith("}"):
            print("accolades [%d:%d]: %r" % (i, j, sub))
# essai: un caractere sur deux, en partant de chaque offset
for off in range(3):
    print("offset %d, pas 2: %r" % (off, s[off::2]))
print("\nrecherche 'academy' :", s.find("academy"))
print("recherche 'cademy'  :", s.find("cademy"))
# union: caracteres uniques dans l'ordre
seen = []
for ch in s:
    if ch not in seen:
        seen.append(ch)
print("uniques:", "".join(seen))
