#!/bin/bash
ls -la /usr/share/wordlists/ 2>/dev/null | head -10
for f in /usr/share/wordlists/rockyou.txt /usr/share/wordlists/rockyou.txt.gz /usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-10000.txt; do
  [ -e "$f" ] && echo "PRESENT: $f"
done
echo "--- hashcat/john ? ---"
which hashcat john 2>/dev/null
echo "--- test rapide de mots de passe courants ---"
python3 - <<'EOF'
import hashlib
targets = {
 "5a9a79d9fa477ed163b89088681672c9":"admin",
 "7a67ab5872843b22b5e14511867c4e43":"ctf-player",
}
words = ["admin","password","123456","admin123","picoctf","cylab","secret","letmein","qwerty",
         "flag","ctf","root","toor","admin1234","Password1","administrator","password1","12345678",
         "welcome","iloveyou","monkey","dragon","abc123","pass","test","demo","hacker","user"]
for w in words:
    h = hashlib.md5(w.encode()).hexdigest()
    if h in targets:
        print("TROUVE:", targets[h], "->", w)
EOF
