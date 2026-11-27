import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
r = requests.get("https://raw.githubusercontent.com/Cajac/picoCTF-Writeups/089132895784747dec04339d147b73609193f45f/picoCTF_2019/Forensics/Investigative_Reversing_0.md",
                 timeout=30, verify=False, headers={"User-Agent": "Mozilla/5.0"})
t = r.text
print("HTTP", r.status_code, "len", len(t))
i = t.find("## Solution")
print(t[i:i + 3000] if i >= 0 else t[:3000])
