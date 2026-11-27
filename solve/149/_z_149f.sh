#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_re || exit 1
refs() {
  setarch -R valgrind --tool=cachegrind --cachegrind-out-file=/dev/null ./149_checkpass "$1" 2>&1 | grep -E 'I +refs' | head -1 | sed 's/.*refs: *//; s/,//g'
}
echo "run1 academy{AAA: $(refs 'academy{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}')"
echo "run2 academy{AAA: $(refs 'academy{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}')"
echo "run3 academy{AAA: $(refs 'academy{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}')"
echo "acadXmy: $(refs 'acadXmy{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}')"
