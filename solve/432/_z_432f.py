import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/089132895784747dec04339d147b73609193f45f/picoCTF_2024/Forensics/Blast_from_the_past.md",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
print("longueur:", len(t))
for kw in ("Thumbnail", "flag", "modif", "nc ", "Orientation", "###"):
    idxs = [m.start() for m in re.finditer(re.escape(kw), t)]
    print(kw, "->", idxs[:8])
print("\n=== fin du document ===")
print(t[-2500:])
