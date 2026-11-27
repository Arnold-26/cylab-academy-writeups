import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://omar-4.gitbook.io/omar-khalid/pages/ctf-writeups/forensics-challenge-dear-diary-or-picoctf-writeup",
          "https://picoctfsolutions.com/picoctf-2023-dear-diary"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 4]
        print("##### " + u[-38:])
        for l in lines[:55]:
            print("  ", l[:190])
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
