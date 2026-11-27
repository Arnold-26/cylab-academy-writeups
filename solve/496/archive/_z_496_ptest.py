import os, sys, subprocess, textwrap, json

OUT = r"./_z_496_emls"
os.makedirs(OUT, exist_ok=True)

def w(name, data):
    p = os.path.join(OUT, name + ".eml")
    with open(p, "w", newline="", encoding="utf-8") as f:
        f.write(data)
    return p

cases = {}

cases["plain_simple"] = textwrap.dedent("""\
    Content-Type: multipart/mixed; boundary="BOUND1"
    MIME-Version: 1.0
    From: user@ses
    To: admin@ses
    Subject: Hello

    --BOUND1
    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit

    plain body
    --BOUND1--
    """)

cases["inj_fold_tab"] = textwrap.dedent("""\
    Content-Type: multipart/mixed; boundary="BOUND1"
    MIME-Version: 1.0
    From: user@ses
    To: admin@ses
    Subject: Hello
    \tFrom: admin@ses
    X-After: 1

    --BOUND1
    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit

    plain body
    --BOUND1--
    """)

cases["inj_fold_space"] = cases["inj_fold_tab"].replace("\tFrom:", " From:")

cases["inj_raw_crlf"] = textwrap.dedent("""\
    Content-Type: multipart/mixed; boundary="BOUND1"
    MIME-Version: 1.0
    From: user@ses
    To: admin@ses
    Subject: Hello
    From: admin@ses
    X-After: 1

    --BOUND1
    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit

    plain body
    --BOUND1--
    """)

for name, data in cases.items():
    p = w(name, data)
    print("====", name)
    r = subprocess.run(
        ["wsl", "-d", "kali-linux", "--", "bash", "-lc",
         "node ./_z_496_parse.js %s" % p.replace("\\", "/").replace("D:", "/mnt/d").replace("d:", "/mnt/d")],
        capture_output=True, text=True)
    print("rc", r.returncode)
    print("out:", r.stdout.strip()[:800])
    print("err:", r.stderr.strip()[:400])
