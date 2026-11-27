import socket, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT, FMT = sys.argv[1], int(sys.argv[2]), sys.argv[3].encode()

s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(1.0)
time.sleep(0.25)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"1\n")
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
t0 = time.time()
s.sendall(FMT + b"\n")
total = 0
last = t0
while time.time() - t0 < 120:
    try:
        d = s.recv(1 << 20)
    except socket.timeout:
        if time.time() - last > 5:
            print("stall de 5 s, arret")
            break
        continue
    except Exception as e:
        print("exception:", e)
        break
    if not d:
        print("EOF du serveur a t=%.2fs" % (time.time() - t0))
        break
    total += len(d)
    last = time.time()
    if total % (1 << 20) < len(d):
        print("  t=%.2fs  %d octets  (%.0f Ko/s)" % (time.time() - t0, total, total / 1024 / (time.time() - t0)))
s.close()
dt = time.time() - t0
print("TOTAL %d octets en %.2fs = %.0f Ko/s" % (total, dt, total / 1024 / dt))
