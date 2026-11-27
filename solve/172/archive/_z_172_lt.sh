#!/bin/bash
cd /tmp/office
echo "=== ltrace sur option 4 (employe non admin) ==="
printf '1\nBob\nn\n1000\n111\nn\n4\n0\n0\n' > in4.txt
ltrace -f -e 'fopen+fgets+printf+puts+strcmp+__isoc99_scanf' ./the_office < in4.txt 2>&1 | head -30
