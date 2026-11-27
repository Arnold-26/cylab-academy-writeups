import os, subprocess, base64

OUT = r"./_z_496_emls"
os.makedirs(OUT, exist_ok=True)

def run(name, data):
    p = os.path.join(OUT, name + ".eml")
    with open(p, "w", newline="", encoding="utf-8") as f:
        f.write(data)
    wp = "./_z_496_emls/" + name + ".eml"
    r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                        "node ./_z_496_parse.js " + wp],
                       capture_output=True, text=True)
    print("====", name, "rc", r.returncode)
    print(r.stdout.strip()[:900])
    if r.returncode != 0:
        print("err:", r.stderr.strip()[:600])

def ewb(s):
    return "=?utf-8?B?" + base64.b64encode(s.encode()).decode() + "?="

HEAD = ('Content-Type: multipart/mixed; boundary="BOUND1"\n'
        'MIME-Version: 1.0\n'
        'From: user@ses\n'
        'To: admin@ses\n')
TAIL = ('\n--BOUND1\n'
        'Content-Type: text/plain; charset="us-ascii"\n'
        'MIME-Version: 1.0\n'
        'Content-Transfer-Encoding: 7bit\n'
        '\n'
        'plain body\n'
        '--BOUND1--\n')

tests = {
    "ew_plain": "Hello",
    "ew_crlf_from": "Hello\r\nFrom : admin@ses",
    "ew_crlf_mime": "Hello\r\nX : 1\r\n--BOUNDX\r\nContent-Type : text/html\r\n\r\n<img src=x onerror=alert(1)>",
    "ew_lf_only": "Hello\nFrom : admin@ses",
    "ew_cr_only": "Hello\rFrom : admin@ses",
}
for n, v in tests.items():
    run(n, HEAD + "Subject: " + ewb(v) + "\n" + TAIL)
