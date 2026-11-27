import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
try:
    import websocket
except ImportError:
    print("websocket-client absent")
    sys.exit(1)
url = "ws://xebec.cylabacademy.net:30999/ws/"
try:
    ws = websocket.create_connection(url, timeout=15, origin="http://xebec.cylabacademy.net:30999")
    print("connecte")
    msgs = ["eval -99999", "mate -99999", "eval -1000000", "mate 1", "eval 99999"]
    for m in msgs:
        ws.send(m)
        try:
            ws.settimeout(3)
            resp = ws.recv()
            print(f"{m!r} -> {resp!r}")
        except Exception as e:
            print(f"{m!r} -> (pas de reponse: {type(e).__name__})")
    ws.close()
except Exception as e:
    print("err", type(e).__name__, e)
