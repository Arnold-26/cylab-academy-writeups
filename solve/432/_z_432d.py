import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/089132895784747dec04339d147b73609193f45f/picoCTF_2024/Forensics/Blast_from_the_past.md",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
print("HTTP", r.status_code, len(r.text))
print(r.text[:2500])
