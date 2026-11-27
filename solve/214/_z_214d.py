import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://netorika.medium.com/picoctf-lockdown-horses-binary-exploitation-writeup-a27c13c3b752",
          "https://hackmd.io/@trhoanglan04/pico_ctf"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip() and len(l.strip()) > 4]
        print("##### " + u[-36:])
        hit = False
        for i, l in enumerate(lines):
            if "lockdown" in l.lower() or "horse" in l.lower():
                hit = True
            if hit:
                for x in lines[i:i+40]:
                    print("  ", x[:190])
                break
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
