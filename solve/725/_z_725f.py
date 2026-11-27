import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
H = {"User-Agent": "Mozilla/5.0"}
urls = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=is&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=is&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/countries/IS/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
]
found = []
for u in urls:
    try:
        r = requests.get(u, timeout=25, headers=H, verify=False)
        txt = r.text.strip()
        print("### %s -> %s (%d o)" % (u.split("?")[0][-45:], r.status_code, len(txt)))
        lines = [l.strip() for l in txt.splitlines() if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", l.strip())]
        print("   proxys:", len(lines), lines[:6])
        if "IS/" in u or "country=is" in u:
            found.extend(lines)
    except Exception as e:
        print("### ERR", type(e).__name__, u[:60])
print("\nISLANDE trouves:", found[:10])
