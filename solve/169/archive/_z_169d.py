import sys, requests, urllib3, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
for path in ("examples/free", "examples"):
    u = "https://api.github.com/repos/corkami/collisions/contents/" + path
    try:
        r = requests.get(u, timeout=25, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        print("===", path, r.status_code)
        if r.status_code == 200:
            for it in r.json():
                print("   ", it["type"], it["name"], it.get("size"))
        else:
            print("   ", r.text[:120])
    except Exception as e:
        print(path, "ERR", type(e).__name__)
