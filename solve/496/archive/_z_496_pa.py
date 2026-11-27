import sys
sys.path.insert(0, r'.')
from _z_496_prob import run

# A1: multipart/mixed text/plain + text/html
run('a1', (
 'Content-Type: multipart/mixed; boundary="XY"\nMIME-Version: 1.0\n\n'
 '--XY\nContent-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
 'AAA plain\n'
 '--XY\nContent-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n'
 '<b>BBB html</b>\n'
 '--XY--\n'))

# A2: two text/html parts
run('a2', (
 'Content-Type: multipart/mixed; boundary="XY"\nMIME-Version: 1.0\n\n'
 '--XY\nContent-Type: text/html; charset="us-ascii"\n\n'
 'FIRST-HTML\n'
 '--XY\nContent-Type: text/html; charset="us-ascii"\n\n'
 'SECOND-HTML\n'
 '--XY--\n'))

# A3: multipart/mixed with only text/plain
run('a3', (
 'Content-Type: multipart/mixed; boundary="XY"\nMIME-Version: 1.0\n\n'
 '--XY\nContent-Type: text/plain; charset="us-ascii"\n\n'
 'ONLY-PLAIN\n'
 '--XY--\n'))

# A4: whole message text/html
run('a4', 'Content-Type: text/html; charset="us-ascii"\n\n<h1>WHOLE</h1>\n')

# A5: text/plain + text/html + text/html
run('a5', (
 'Content-Type: multipart/mixed; boundary="XY"\n\n'
 '--XY\nContent-Type: text/plain\n\nP0\n'
 '--XY\nContent-Type: text/html\n\nH1\n'
 '--XY\nContent-Type: text/html\n\nH2\n'
 '--XY--\n'))
