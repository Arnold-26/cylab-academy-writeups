import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://mh4ck3r0n3.github.io/posts/2025/03/20/pachinko/index.md",
          "https://hackingwithmaulik.hashnode.dev/pachinko.md"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = html.unescape(r.text)
        if r.status_code != 200:
            print(u[-40:], r.status_code)
            continue
        print("##### " + u[-40:], len(t))
        # chercher les parties interessantes
        for kw in ("flag2", "FLAG2", "flag two", "second flag", "cpu.json", "nand", "circuit"):
            for m in list(re.finditer(kw, t, re.I))[:2]:
                seg = re.sub(r"\s+", " ", t[max(0, m.start()-250):m.start()+350])
                print("[%s] %s" % (kw, seg[:400]))
        print("=== flags trouves ===")
        for m in re.finditer(r"(?:academy|picoCTF)\{[^}]{3,120}\}", t):
            print(" ", m.group(0))
    except Exception as e:
        print("ERR", type(e).__name__)
