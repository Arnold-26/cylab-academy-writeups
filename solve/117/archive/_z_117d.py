import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
for u in ("https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/main/picoCTF_2021/Forensics/Surfing_the_Waves.md",
          "https://picoctf2021.haydenhousen.com/forensics/surfing-the-waves.md"):
    try:
        r = requests.get(u, timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        t = r.text
        print("##### %s (%s, %d)" % (u[-45:], r.status_code, len(t)))
        i = t.find("Solution")
        seg = t[i:i + 1800] if i >= 0 else t[:1800]
        print(seg)
        print()
    except Exception as e:
        print("ERR", type(e).__name__)
