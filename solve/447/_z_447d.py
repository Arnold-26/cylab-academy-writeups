import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://mh4ck3r0n3.github.io/posts/2025/03/09/elements/index.md",
          "https://kevins-organization-14.gitbook.io/picoctf-writeup/web-exploitation/picoctf-2024/elements.md"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            print(u[-45:], r.status_code)
            continue
        t = html.unescape(r.text)
        print("##### " + u[-45:], len(t))
        print(t[:3500])
        print("=== flags ===")
        for m in re.finditer(r"(?:picoCTF|academy)\{[^}]{3,140}\}", t):
            print(" ", m.group(0))
    except Exception as e:
        print("ERR", type(e).__name__)
