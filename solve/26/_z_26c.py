import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/refs/heads/main/picoCTF_2019/Forensics/m00nwalk.md",
          "https://picoctfsolutions.com/picoctf-2019-m00nwalk"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        if not u.endswith(".md"):
            t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
            t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 4]
        print("##### " + u[-34:])
        for l in lines[:40]:
            print("  ", l[:190])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
