#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 181_vuln 2>/dev/null
echo "=== essai : 1, 2, fizz, 4, buzz ==="
printf '1\n2\nfizz\n4\nbuzz\n' | timeout 5 ./181_vuln 2>&1 | head -12
echo
echo "=== essai : 1, 2, Fizz, 4, Buzz ==="
printf '1\n2\nFizz\n4\nBuzz\n' | timeout 5 ./181_vuln 2>&1 | head -12
echo
echo "=== essai : nombres seuls 1..8 ==="
printf '1\n2\n3\n4\n5\n6\n7\n8\n' | timeout 5 ./181_vuln 2>&1 | head -14
