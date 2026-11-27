import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/3c5c988dd57a015e11edd6c25b8398269ec57257/picoCTF_2023/Reverse_Engineering/Ready_Gladiator_2.md",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
print("HTTP", r.status_code)
print(r.text[:2500])
