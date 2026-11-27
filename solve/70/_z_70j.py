import sys, json, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=1.5)
cy.login()
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 70,
                                             "flag": "academy{f0und_1t_54c420aa}"})
print("status:", st)
t = re.sub(r"<[^>]+>", " ", b)
t = re.sub(r"\s+", " ", t)
print("corps:", t[:400])
st2, b2 = cy.req("GET", "/api/challenges/70/")
print("\nGET status:", st2, "| debut:", b2[:120])
