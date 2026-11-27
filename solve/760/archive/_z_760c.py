import sys, requests, re, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for port in (22404, 29641):
    try:
        r = requests.get(f"http://xebec.cylabacademy.net:{port}/", timeout=25, verify=False)
        t = r.text
        t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<script.*?</script>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        print(f"=== :{port} ===")
        for l in lines[:40]:
            print("  ", l[:160])
    except Exception as e:
        print(port, "ERR", type(e).__name__)
    print()
