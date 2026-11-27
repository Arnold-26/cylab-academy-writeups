import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
urls = [
 "https://raw.githubusercontent.com/HHousen/PicoCTF-2021/2f534a3d0f0276af8097ba1b90004c2b89a82528/Web%20Exploitation/Some%20Assembly%20Required%204/README.md",
 "https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Web%20Exploitation/Some%20Assembly%20Required%204/README.md",
 "https://hawksec.gitbook.io/pt/writeups/picoctf/web-exploitation/some_assembly_required.md",
 "https://eylau-ucsd.github.io/blog/2022/09/08/Dabbling-in-CTFs.html",
]
for u in urls:
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        if r.status_code != 200:
            print(u[-45:], r.status_code)
            continue
        if not u.endswith(".md"):
            t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
            t = re.sub(r"<[^>]+>", "\n", t)
        t = html.unescape(t)
        flags = list(re.finditer(r"(?:picoCTF|academy)\{[^}]{3,140}\}", t))
        print("##### " + u[-45:], "| flags:", [m.group(0) for m in flags])
        for kw in ("SAR4", "flag", "xor", "byte", "shift"):
            for m in list(re.finditer(kw, t, re.I))[:1]:
                seg = re.sub(r"\s+", " ", t[max(0, m.start()-200):m.start()+300])
                print("   [%s] %s" % (kw, seg[:330]))
    except Exception as e:
        print(u[-35:], "ERR", type(e).__name__)
