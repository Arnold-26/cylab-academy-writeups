#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
printf 'AAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAA\n' > /tmp/in217.txt
timeout 20 ./217_homework < /tmp/in217.txt > /tmp/out217.txt 2> /tmp/err217.txt
echo "exit: $?"
echo "=== stdout ==="
cat /tmp/out217.txt
echo "=== stderr ==="
cat /tmp/err217.txt
echo "=== strings du prompt ==="
strings -n 4 217_homework | sed -n '/Enter homework/,+3p'
