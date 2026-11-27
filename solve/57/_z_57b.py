import sys, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

p = r"/tmp/cylab_eps\57_win-exec-1.exe"
d = open(p, "rb").read()
needle = b"academy{"
i = d.find(needle)
print("offset:", i)
print("extrait 200 octets:", repr(d[i:i+200]))
# la chaine complete jusqu'au NUL
end = d.find(b"\x00", i)
print("chaine jusqu'au NUL (%d octets):" % (end - i), repr(d[i:end]))
# on tente aussi un decoupage sur les separateurs classiques
for m in re.finditer(rb"academy\{[ -~]{0,120}", d):
    print("  candidat:", repr(m.group(0)))
