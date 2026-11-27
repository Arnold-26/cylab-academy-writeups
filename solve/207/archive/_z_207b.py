import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
for cid in (207, 211):
    d = Path(r"/tmp/cylab_eps\pm_%d" % cid)
    key = (d / "private.key").read_text(errors="replace")
    enc = (d / "msg.enc").read_bytes()
    print("=== %d ===" % cid)
    print("msg.enc:", len(enc), "octets | hex:", enc[:32].hex(), "...")
    print("cle:", key.splitlines()[0][:60], "...", len(key), "octets")
    # compter les lignes et reperer une ligne suspecte (longueur anormale)
    body = [l for l in key.splitlines() if l and not l.startswith("-----")]
    print("lignes base64:", len(body), "| longueurs:", sorted(set(len(l) for l in body)))
    for i, l in enumerate(body):
        if len(l) == 64 and not re.fullmatch(r"[A-Za-z0-9+/=]+", l):
            print("   ligne suspecte", i, repr(l))
        if " " in l or "\t" in l:
            print("   ESPACE ligne", i, repr(l[:70]))
