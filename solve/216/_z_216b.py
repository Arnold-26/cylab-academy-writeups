import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31890

tests = [b"0xdeadbeef\n", b"3735928559\n", b"deadbeef\n", b"\xef\xbe\xad\xde\n",
         b"A" * 20 + b"\n", b"A" * 64 + b"\n", b"A" * 128 + b"\n"]
for payload in tests:
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(4)
        time.sleep(0.6)
        try:
            s.recv(8192)
        except Exception:
            pass
        s.sendall(payload)
        time.sleep(0.8)
        out = b""
        try:
            out = s.recv(8192)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        print(f"--- {payload[:24]!r} ---")
        print(txt[-300:])
        s.close()
    except Exception as e:
        print(payload[:20], "err", type(e).__name__)
