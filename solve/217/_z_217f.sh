#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo 'academy{TESTLOCAL123}' > flag.txt
cat > /tmp/bef.txt <<'EOF'
0!:+:+::**00p00g00!:v
v+:::!0p<+++::*:+::+<
>:++:+:+ +:0>0gg,:v
00g0!-00^ ^0:-!0_
EOF
echo "=== local ==="
timeout 20 ./217_homework < /tmp/bef.txt 2>&1 | head -5
echo "=== exit: $? ==="
