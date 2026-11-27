import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 47902

RULES = {
    "writeup exact": '''rule Rule{
    strings:
        $str1 = {4D 5A}
        $str2 = "YaraRules0x100"
        $str3 = "UPX"
        $str4 = "NtQuery"
        $str5 = "debugger process" wide ascii

    condition:
        ($str1 and $str2 and ($str3 or $str4)) or $str5
}
''',
    "renforcee": '''rule CyLab_FakeMalware
{
    strings:
        $mz = {4D 5A}
        $name1 = "YaraRules0x100" ascii wide
        $upx = "UPX" ascii
        $ntq = "NtQuery" ascii
        $dbg = "debugger process" wide ascii
        $fake = "fake malware" wide ascii nocase
        $oop = "Debugger Detected" wide ascii
    condition:
        $mz and ($name1 or $fake) and ($upx or $ntq or $dbg or $oop)
}
''',
}


def submit(data, label):
    print("=== %s ===" % label)
    try:
        s = socket.create_connection((HOST, PORT), timeout=30)
        s.settimeout(60)
        s.sendall(data.encode() if isinstance(data, str) else data)
        time.sleep(0.4)
        s.shutdown(socket.SHUT_WR)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 60:
            try:
                c = s.recv(16384)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        txt = out.decode("utf-8", "replace")
        print(txt[:800])
        f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        return f.group(0) if f else None
    except Exception as e:
        print("ERR", type(e).__name__)
        return None


for label, rule in RULES.items():
    fl = submit(rule, label)
    if fl:
        print("FLAG:", fl)
        break
    print()
