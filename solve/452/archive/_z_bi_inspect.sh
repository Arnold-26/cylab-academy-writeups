#!/bin/bash
cd /tmp/bi
for f in bininst1_payload.bin bininst2_payload.bin; do
  echo "===== $f"
  file "$f"
  echo "--- sections ---"
  objdump -h "$f" | sed -n '5,20p'
done
echo "===== strings bininst1 (interessants) ====="
strings -a bininst1_payload.bin | grep -i -E 'academy|flag|frida|condition|wake|sleep' | head -30
echo "===== strings bininst2 (interessants) ====="
strings -a bininst2_payload.bin | grep -i -E 'academy|flag|writefile|createfile|error|failed' | head -30
