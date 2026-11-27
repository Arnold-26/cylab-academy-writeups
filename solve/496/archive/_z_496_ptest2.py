import os, subprocess, textwrap

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
    print(r.stdout.strip()[:600])
    if r.returncode != 0:
        print("err:", r.stderr.strip()[:400])

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

cases = {
    "s_plain":      "Subject: Hello\n",
    "s_spacecolon": "Subject: Hello\nFrom : admin@ses\n",
    "s_tabcolon":   "Subject: Hello\nFrom\t: admin@ses\n",
    "s_tabtab":     "Subject: Hello\nFrom:\tadmin@ses\n",
    "s_2from":      "Subject: Hello\nFrom : admin@ses\nFrom : admin@ses\n",
}
for n, s in cases.items():
    run(n, HEAD + s + TAIL)
