import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 12383
RATIO = 9359
s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(8)
time.sleep(0.5)
data = s.recv(8192).decode("utf-8", "replace")
print("prompt:", data)
nums = re.findall(r"\d+", data)
print("nombres:", nums)
if not nums:
    print("pas de nombre")
    s.close()
    sys.exit(1)
n = int(nums[-1])
ans = n * RATIO
print(f"{n} * {RATIO} = {ans}")
s.sendall((str(ans) + "\n").encode())
time.sleep(0.8)
out = b""
try:
    while True:
        c = s.recv(8192)
        if not c:
            break
        out += c
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("=== REPONSE ===")
print(txt[:800])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", f.group(0) if f else "non trouve")
s.close()
