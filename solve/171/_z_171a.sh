#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 171_enter_password
file 171_enter_password | cut -c1-120
echo "=== chaines interessantes ==="
strings -n 6 171_enter_password | grep -aiE "password|enter|correct|wrong|flag|input" | head -20
echo "=== symboles main ==="
go tool nm 171_enter_password 2>/dev/null | grep -E " main\." | head -20 || nm 171_enter_password 2>/dev/null | grep -i "main" | head -10
