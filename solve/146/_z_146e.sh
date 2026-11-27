#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
printf 'academy{LOCAL_TEST}\n' > flag.txt
cat > /tmp/g146.gdb <<'EOF'
set pagination off
break *0x4009c5
run < /dev/null
printf "chunk1 (rbp-0x98) = %p\n", *(void**)($rbp-0x98)
printf "chunk8 (rbp-0x80) = %p\n", *(void**)($rbp-0x80)
printf "chunk7 (rbp-0x90) = %p\n", *(void**)($rbp-0x90)
info proc mappings
quit
EOF
gdb -nx -q -batch -x /tmp/g146.gdb ./146_heapedit 2>&1 | tail -25
