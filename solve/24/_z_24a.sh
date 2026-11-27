#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_re || exit 1
cat > /tmp/gdb24.txt <<'EOF'
set pagination off
break doNothing
commands
silent
printf "ARG=%d\n", *(int*)($esp+4)
continue
end
run
EOF
timeout 120 gdb -nx -q -batch -x /tmp/gdb24.txt ./24_vuln 2>&1 | grep 'ARG=' | tail -5
