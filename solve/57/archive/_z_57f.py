import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://raw.githubusercontent.com/Dvd848/CTFs/80a837a89d2174b649b029aed092e3b5ecf073e6/2019_picoCTF/B1ll_Gat35.md",
          "https://picoctfsolutions.com/picoctf-2019-b1ll-gat35"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        if not u.endswith(".md"):
            t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
            t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 3]
        print("##### " + u[-38:])
        for l in lines[:45]:
            print("  ", l[:190])
        print("=== flags ===")
        for m in re.finditer(r"(?:picoCTF|academy)\{[^}]{3,200}\}", t):
            print(" ", m.group(0))
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
