#!/bin/bash
which pmars || (echo userd | sudo -S apt-get install -y -qq pmars 2>&1 | tail -2; which pmars)
mkdir -p /tmp/cw && cd /tmp/cw || exit 1
printf ';redcode\n;name Imp\n;assert 1\nmov 0, 1\nend\n' > imp.red
cat > herem.red <<'EOF'
;redcode-94
;name Herem
bomb       dat #4, #4
start      add.ab #4, bomb
           mov.i   bomb, @bomb
           jmp     start
end start
EOF
echo "=== herem vs imp (100 rondes) ==="
timeout 120 pmars -r 100 -b herem.red imp.red 2>&1 | tail -8
